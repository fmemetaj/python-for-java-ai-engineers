from course_kit.loader import load_concept_module

skip = load_concept_module("0_05", "skip")


def test_empty_list_is_falsy() -> None:
    assert skip.empty_list_is_true() is False


def test_string_zero_is_truthy() -> None:
    assert skip.string_zero_is_true() is True
