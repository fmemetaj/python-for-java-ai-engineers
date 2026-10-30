from course_kit.loader import load_concept_module

skip = load_concept_module("0_24", "skip")


def test_python_has_checked_exceptions() -> None:
    assert skip.python_has_checked_exceptions() is False


def test_raise_from_chains() -> None:
    assert skip.raise_from_chains() is True
