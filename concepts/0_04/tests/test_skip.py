from course_kit.loader import load_concept_module

skip = load_concept_module("0_04", "skip")


def test_none_is_not_empty_string() -> None:
    assert skip.none_equals_empty_string() is False


def test_int_is_unbounded() -> None:
    assert skip.python_int_overflows_like_java_int() is False
