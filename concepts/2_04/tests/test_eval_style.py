import pytest
from course_kit.loader import load_concept_module

style = load_concept_module("2_04", "eval_style")


def test_behavior_targets() -> None:
    assert style.assert_strategy("cost") == "behavior"
    assert style.assert_strategy("usage_shape") == "behavior"
    assert style.assert_strategy("json_schema") == "behavior"


def test_forbidden_wording() -> None:
    assert style.assert_strategy("live_wording") == "forbidden"


def test_unknown() -> None:
    with pytest.raises(ValueError):
        style.assert_strategy("vibes")
