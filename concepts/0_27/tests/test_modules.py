import pytest
from course_kit.loader import load_concept_module

mod = load_concept_module("0_27", "modules")


def test_module_stem() -> None:
    assert mod.module_stem("log_stats.py") == "log_stats"
    with pytest.raises(ValueError):
        mod.module_stem("log_stats")


def test_dunder_init() -> None:
    assert mod.is_dunder_init("__init__.py") is True
    assert mod.is_dunder_init("tools.py") is False


def test_package_parts() -> None:
    assert mod.package_parts("mini_agent.tools") == ["mini_agent", "tools"]
    assert mod.package_parts("mini_agent") == ["mini_agent"]
