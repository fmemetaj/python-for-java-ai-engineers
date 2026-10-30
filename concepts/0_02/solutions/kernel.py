"""Simulate Jupyter kernel assignment order (solution)."""

from __future__ import annotations


def last_value(assignments: list[tuple[str, object]], name: str) -> object:
    """Return the value bound to `name` after applying assignments in order."""
    current: dict[str, object] = {}
    for key, value in assignments:
        current[key] = value
    return current[name]


def missing_after_partial_run(defined: list[str], referenced: str) -> bool:
    """Return True if `referenced` was never assigned in the executed cells."""
    return referenced not in set(defined)
