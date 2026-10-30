"""Filter and default using Python truthiness (solution)."""

from __future__ import annotations


def keep_truthy(values: list[object]) -> list[object]:
    """Return values that are true in a boolean context, in the same order."""
    return [value for value in values if value]


def first_present(*values: object) -> object | None:
    """Return the first truthy value, or None if all are falsy."""
    for value in values:
        if value:
            return value
    return None
