from course_kit.loader import load_concept_module
import pytest

pyproject = load_concept_module("1_02", "pyproject")


def test_dependency_line() -> None:
    assert pyproject.dependency_line("httpx", "0.27", "1") == "httpx>=0.27,<1"


def test_compile_scope() -> None:
    assert pyproject.group_for_maven_scope("compile") == "project"


def test_test_scope() -> None:
    assert pyproject.group_for_maven_scope("test") == "dev"


def test_optional_scope() -> None:
    assert pyproject.group_for_maven_scope("optional") == "demo"


def test_unknown_scope() -> None:
    with pytest.raises(ValueError):
        pyproject.group_for_maven_scope("provided")


def test_stale_lock() -> None:
    msg = "Unable to sync: The lockfile at `uv.lock` needs to be updated, it is out of date."
    assert pyproject.diagnose_lock_error(msg) == "run uv lock and commit uv.lock"
