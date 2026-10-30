from course_kit.loader import load_concept_module

skip = load_concept_module("1_05", "skip")


def test_ruff_role() -> None:
    assert skip.ruff_is_the_style_linter() is True


def test_pyright_not_runtime() -> None:
    assert skip.pyright_enforces_types_at_runtime() is False
