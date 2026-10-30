"""Import path helpers (solution)."""

from __future__ import annotations


def module_stem(file_name: str) -> str:
    """'log_stats.py' -> 'log_stats'. Reject names without a .py suffix via ValueError."""
    if not file_name.endswith(".py"):
        raise ValueError(f"not a python file: {file_name}")
    return file_name[: -len(".py")]


def is_dunder_init(file_name: str) -> bool:
    """True for '__init__.py'."""
    return file_name == "__init__.py"


def package_parts(dotted: str) -> list[str]:
    """'mini_agent.tools' -> ['mini_agent', 'tools']."""
    return dotted.split(".")
