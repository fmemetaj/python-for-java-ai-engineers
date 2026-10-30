"""Simulate Jupyter kernel assignment order."""

from __future__ import annotations


def last_value(assignments: list[tuple[str, object]], name: str) -> object:
    """Return the value bound to `name` after applying assignments in order."""
    raise NotImplementedError


def missing_after_partial_run(defined: list[str], referenced: str) -> bool:
    """Return True if `referenced` was never assigned in the executed cells."""
    raise NotImplementedError
