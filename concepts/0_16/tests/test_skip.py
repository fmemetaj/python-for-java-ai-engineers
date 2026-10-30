from course_kit.loader import load_concept_module

skip = load_concept_module("0_16", "skip")


def test_python_has_private_keyword() -> None:
    assert skip.python_has_private_keyword() is False


def test_init_is_the_constructor() -> None:
    assert skip.init_is_the_constructor() is True
