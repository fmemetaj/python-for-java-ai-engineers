from course_kit.loader import load_concept_module
import pytest

lint = load_concept_module("1_05", "lint")


def test_unused_import() -> None:
    assert lint.tool_for("unused-import") == "ruff"


def test_line_too_long() -> None:
    assert lint.tool_for("line-too-long") == "ruff"


def test_type_mismatch() -> None:
    assert lint.tool_for("type-mismatch") == "pyright"


def test_unknown_issue() -> None:
    with pytest.raises(ValueError):
        lint.tool_for("spotbugs")


def test_not_runtime() -> None:
    assert lint.pyright_is_runtime_enforcement() is False
