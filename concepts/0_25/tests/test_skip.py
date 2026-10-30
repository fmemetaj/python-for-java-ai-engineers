from course_kit.loader import load_concept_module

skip = load_concept_module("0_25", "skip")


def test_with_always_closes() -> None:
    assert skip.with_always_closes() is True


def test_writing_one_needs_enter_exit() -> None:
    assert skip.writing_one_needs_enter_exit() is True
