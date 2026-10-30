from course_kit.loader import load_concept_module

skip = load_concept_module("0_26", "skip")


def test_decorator_runs_code() -> None:
    assert skip.decorator_runs_code() is True


def test_annotation_is_the_same() -> None:
    assert skip.annotation_is_the_same() is False
