from course_kit.loader import load_concept_module

skip = load_concept_module("0_23", "skip")


def test_hints_enforced_at_runtime() -> None:
    assert skip.hints_enforced_at_runtime() is False


def test_pyright_is_static() -> None:
    assert skip.pyright_is_static() is True
