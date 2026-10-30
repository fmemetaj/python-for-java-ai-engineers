import pytest
from course_kit.loader import load_concept_module

exc_mod = load_concept_module("0_24", "exceptions")


def test_parse_level() -> None:
    assert exc_mod.parse_level("ERROR disk") == "ERROR"
    with pytest.raises(exc_mod.ParseError):
        exc_mod.parse_level("   ")


def test_default() -> None:
    assert exc_mod.parse_level_or_default("WARNING slow") == "WARNING"
    assert exc_mod.parse_level_or_default("") == "INFO"


def test_chaining() -> None:
    with pytest.raises(ValueError) as err:
        exc_mod.wrap_parse("")
    assert err.value.__cause__ is not None
    assert isinstance(err.value.__cause__, exc_mod.ParseError)
