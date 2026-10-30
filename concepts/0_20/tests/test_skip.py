from course_kit.loader import load_concept_module

skip = load_concept_module("0_20", "skip")


def test_python_allows_multiple_inheritance() -> None:
    assert skip.python_allows_multiple_inheritance() is True


def test_mro_is_linear() -> None:
    assert skip.mro_is_linear() is True
