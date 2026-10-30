from course_kit.loader import load_concept_module

tradeoff = load_concept_module("2_11", "tradeoff")


def test_cheaper() -> None:
    assert tradeoff.cheaper_effort("none", 2, "high", 258) == "none"
    assert tradeoff.cheaper_effort("high", 258, "none", 2) == "none"
    assert tradeoff.cheaper_effort("low", 10, "medium", 10) == "low"
