"""Filter and default using Python truthiness."""

from __future__ import annotations


def keep_truthy(values: list[object]) -> list[object]:
    """Return values that are true in a boolean context, in the same order."""
    raise NotImplementedError


def first_present(*values: object) -> object | None:
    """Return the first truthy value, or None if all are falsy."""
    raise NotImplementedError
