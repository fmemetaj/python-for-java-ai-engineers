from course_kit.loader import load_concept_module

skip = load_concept_module("0_06", "skip")


def test_range_three() -> None:
    assert skip.range_three() == [0, 1, 2]


def test_for_else_skips_on_break() -> None:
    assert skip.for_else_runs_after_break() is False
