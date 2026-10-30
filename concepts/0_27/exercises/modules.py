"""Import path helpers."""

from __future__ import annotations


def module_stem(file_name: str) -> str:
    """'log_stats.py' -> 'log_stats'. Reject names without a .py suffix via ValueError."""
    raise NotImplementedError


def is_dunder_init(file_name: str) -> bool:
    """True for '__init__.py'."""
    raise NotImplementedError


def package_parts(dotted: str) -> list[str]:
    """'mini_agent.tools' -> ['mini_agent', 'tools']."""
    raise NotImplementedError
