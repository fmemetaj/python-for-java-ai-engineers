import pytest
from course_kit.loader import load_concept_module

effort = load_concept_module("2_11", "effort")


def test_table() -> None:
    assert effort.reasoning_tokens_for(None) == 0
    assert effort.reasoning_tokens_for("none") == 0
    assert effort.reasoning_tokens_for("low") == 16
    assert effort.reasoning_tokens_for("high") == 256


def test_billed() -> None:
    assert effort.billed_output(2, "high") == 258


def test_unknown() -> None:
    with pytest.raises(ValueError):
        effort.reasoning_tokens_for("extreme")
