"""A Hypothesis extension for JSON schemata."""
# pylint: disable=no-value-for-parameter,too-many-return-statements


import re
from typing import Any, Dict, List, Union

from canonicaljson import encode_canonical_json
import jsonschema
from hypothesis import assume
import hypothesis.strategies as st
from hypothesis.errors import InvalidArgument

# Mypy does not (yet!) support recursive type definitions.
# (and writing a few steps by hand is a DoS attack on the AST walker in Pytest)
JSONType = Union[None, bool, float, str, list, dict]

JSON_STRATEGY: st.SearchStrategy[JSONType] = st.deferred(
    lambda: st.one_of(
        st.none(),
        st.booleans(),
        st.floats(allow_nan=False, allow_infinity=False),
        st.text(),
        st.lists(JSON_STRATEGY, max_size=3),
        st.dictionaries(st.text(), JSON_STRATEGY, max_size=3),
    )
)


def from_schema(schema: dict) -> st.SearchStrategy[JSONType]:
    """Take a JSON schema and return a strategy for allowed JSON objects."""
    # Boolean objects are special schemata; False rejects all and True accepts all.
    if schema is False:
        return st.nothing()
    if schema is True:
        return JSON_STRATEGY
    # Otherwise, we're dealing with "objects", i.e. dicts.
    if not isinstance(schema, dict):
        raise InvalidArgument(
            f"Got schema={schema} of type {type(schema).__name__}, "
            "but expected a dict."
        )
    jsonschema.validators.validator_for(schema).check_schema(schema)

    # Now we handle as many validation keywords as we can...
    if schema == {}:
        return JSON_STRATEGY

    if "enum" in schema:
        return st.sampled_from(schema["enum"])
    if "const" in schema:
        return st.just(schema["const"])
    # Schema must have a type then, so:
    if schema["type"] == "null":
        return st.none()
    if schema["type"] == "boolean":
        return st.booleans()
    if schema["type"] in ("number", "integer"):
        return numeric_schema(schema)
    if schema["type"] == "string":
        return string_schema(schema)
    if schema["type"] == "array":
        return array_schema(schema)
    assert schema["type"] == "object"
    return object_schema(schema)


def numeric_schema(schema: dict) -> st.SearchStrategy[float]:
    """Handle numeric schemata."""
    multiple_of = schema.get("multipleOf")
    lower = schema.get("minimum")
    upper = schema.get("maximum")
    if multiple_of is not None or schema["type"] == "integer":
        if lower is not None and schema.get("exclusiveMinimum"):
            lower += 1
        if upper is not None and schema.get("exclusiveMaximum"):
            upper -= 1
        if multiple_of is not None:
            if lower is not None:
                lower += (multiple_of - lower) % multiple_of
                lower //= multiple_of
            if upper is not None:
                upper -= upper % multiple_of
                upper //= multiple_of
            return st.integers(lower, upper).map(
                lambda x: x * multiple_of  # type: ignore
            )
        return st.integers(lower, upper)
    strategy = st.floats(
        min_value=lower, max_value=upper, allow_nan=False, allow_infinity=False
    )
    if schema.get("exclusiveMaximum") or schema.get("exclusiveMinimum"):
        return strategy.filter(lambda x: x not in (lower, upper))
    return strategy


def string_schema(schema: dict) -> st.SearchStrategy[str]:
    """Handle schemata for strings."""
    # also https://json-schema.org/latest/json-schema-validation.html#rfc.section.7
    min_size = schema.get("minLength", 0)
    max_size = schema.get("maxLength")
    if "pattern" in schema:
        if max_size is None:
            max_size = float("inf")
        return st.from_regex(schema["pattern"]).filter(
            lambda s: min_size <= len(s) <= max_size  # type: ignore
        )
    return st.text(min_size=min_size, max_size=max_size)


def array_schema(schema: dict) -> st.SearchStrategy[List[JSONType]]:
    """Handle schemata for arrays."""
    items = schema.get("items", {})
    additional_items = schema.get("additionalItems", {})
    min_size = schema.get("minItems", 0)
    max_size = schema.get("maxItems")
    unique = schema.get("uniqueItems")
    assert "contains" not in schema, "contains is not yet supported"
    if isinstance(items, list):
        min_size = max(0, min_size - len(items))
        if max_size is not None:
            max_size -= len(items)
        fixed_items = st.tuples(*map(from_schema, items))
        extra_items = st.lists(
            from_schema(additional_items), min_size=min_size, max_size=max_size
        )
        return st.tuples(fixed_items, extra_items).map(
            lambda t: list(t[0]) + t[1]  # type: ignore
        )
    if unique:
        return st.lists(
            from_schema(items),
            min_size=min_size,
            max_size=max_size,
            unique_by=encode_canonical_json,
        )
    return st.lists(from_schema(items), min_size=min_size, max_size=max_size)


def object_schema(schema: dict) -> st.SearchStrategy[Dict[str, JSONType]]:
    """Handle a manageable subset of possible schemata for objects."""
    hard_keywords = "dependencies if then else allOf anyOf oneOf not".split()
    assert not any(kw in schema for kw in hard_keywords)

    required = schema.get("required", [])  # required keys
    names = schema.get("propertyNames", {"type": "string"})  # schema for optional keys

    min_size = schema.get("minProperties", 0)
    max_size = schema.get("maxProperties")
    min_size = max(0, min_size - len(required))
    if max_size is not None:
        max_size = max(0, max_size - len(required))

    properties = schema.get("properties", {})  # exact name: value schema
    # patterns = schema.get("patternProperties", {})  # regex for names: value schema
    additional = schema.get("additionalProperties", {})  # schema for other values

    # quick hack, real implementation TBD.
    unconstrained = st.dictionaries(
        string_schema(names),
        from_schema(additional),
        min_size=min_size,
        max_size=max_size,
    )
    if required:

        def combine(dicts: tuple) -> dict:
            d1, d2 = dicts
            assume(set(d1).isdisjoint(d2))
            return {**d1, **d2}

        reqed = st.fixed_dictionaries(
            {k: from_schema(properties.get(k, additional)) for k in required}
        )
        return st.tuples(reqed, unconstrained).map(combine)
    return unconstrained


# OK, now on to the inverse: a strategy for generating schemata themselves.


def json_schemata() -> st.SearchStrategy[Union[bool, Dict[str, JSONType]]]:
    """A Hypothesis strategy for arbitrary JSON schemata."""
    return _json_schemata()


@st.composite
def regex_patterns(draw: Any) -> st.SearchStrategy[str]:
    """A strategy for simple regular expression patterns."""
    fragments = st.one_of(
        st.just("."),
        st.from_regex(r"\[\^?[A-Za-z0-9]+\]"),
        REGEX_PATTERNS.map("{}+".format),
        REGEX_PATTERNS.map("{}?".format),
        REGEX_PATTERNS.map("{}*".format),
    )
    result = draw(st.lists(fragments, min_size=1, max_size=3).map("".join))
    try:
        re.compile(result)
    except re.error:
        assume(False)
    return result  # type: ignore


REGEX_PATTERNS = regex_patterns()


@st.composite
def _json_schemata(draw: Any, *, recur: bool = True) -> Any:
    """Wrapped so we can disable the pylint error in one place only."""
    # Current version of jsonschema does not support boolean schemata,
    # but 3.0 will.  See https://github.com/Julian/jsonschema/issues/337
    unique_list = st.lists(
        JSON_STRATEGY, min_size=1, max_size=10, unique_by=encode_canonical_json
    )
    options = [
        {},
        {"type": "null"},
        {"type": "boolean"},
        gen_number(draw, "integer"),
        gen_number(draw, "number"),
        gen_string(draw),
        {"const": draw(JSON_STRATEGY)},
        {"enum": draw(unique_list)},
    ]
    if recur:
        options.extend([gen_array(draw), gen_object(draw)])
    return draw(st.sampled_from(options))


def gen_number(draw: Any, kind: str) -> Dict[str, Union[str, float]]:
    """Draw a numeric schema."""
    max_int_float = 2 ** 53
    lower = draw(st.none() | st.integers(-max_int_float, max_int_float))
    upper = draw(st.none() | st.integers(-max_int_float, max_int_float))
    if lower is not None and upper is not None and lower > upper:
        lower, upper = upper, lower
    multiple_of = draw(st.none() | st.integers(2, 100))
    assume(None in (multiple_of, lower, upper) or multiple_of <= (upper - lower))
    out: Dict[str, Union[str, float]] = {"type": kind}
    if lower is not None:
        if draw(st.booleans()):
            out["exclusiveMinimum"] = True
            lower -= 1
        out["minimum"] = lower
    if upper is not None:
        if draw(st.booleans()):
            out["exclusiveMaximum"] = True
            upper += 1
        out["maximum"] = upper
    if multiple_of is not None:
        out["multipleOf"] = multiple_of
    return out


def gen_string(draw: Any) -> Dict[str, Union[str, int]]:
    """Draw a string schema."""
    min_size = draw(st.none() | st.integers(0, 10))
    max_size = draw(st.none() | st.integers(0, 1000))
    if min_size is not None and max_size is not None and min_size > max_size:
        min_size, max_size = max_size, min_size
    pattern = draw(st.none() | REGEX_PATTERNS)
    out: Dict[str, Union[str, int]] = {"type": "string"}
    if pattern is not None:
        out["pattern"] = pattern
    if min_size is not None:
        out["minLength"] = min_size
    if max_size is not None:
        out["maxLength"] = max_size
    return out


def gen_array(draw: Any) -> Dict[str, JSONType]:
    """Draw an array schema."""
    min_size = draw(st.none() | st.integers(0, 5))
    max_size = draw(st.none() | st.integers(2, 5))
    if min_size is not None and max_size is not None and min_size > max_size:
        min_size, max_size = max_size, min_size
    items = draw(
        st.builds(dict)
        | _json_schemata(recur=False)
        | st.lists(_json_schemata(recur=False), min_size=1, max_size=10)
    )
    unique = False
    if isinstance(items, list):
        if max_size is not None:
            max_size += len(items)
    else:
        unique = draw(st.booleans())
    out = {"type": "array", "items": items, "uniqueItems": unique}
    if min_size is not None:
        out["minItems"] = min_size
    if max_size is not None:
        out["maxItems"] = max_size
    return out


def gen_object(draw: Any) -> Dict[str, JSONType]:
    """Draw an object schema."""
    out: Dict[str, JSONType] = {"type": "object"}
    required = draw(st.none() | st.lists(st.text(), min_size=1, unique=True))
    min_size = draw(st.none() | st.integers(0, 5))
    max_size = draw(st.none() | st.integers(2, 5))
    if min_size is not None and max_size is not None and min_size > max_size:
        min_size, max_size = max_size, min_size
    if required is not None:
        out["required"] = required
        if min_size is not None:
            min_size += len(required)
        if max_size is not None:
            max_size += len(required)
    if min_size is not None:
        out["minProperties"] = min_size
    if max_size is not None:
        out["maxProperties"] = max_size
    return out
