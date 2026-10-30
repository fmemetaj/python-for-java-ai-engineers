"""Type hints as editor guidance; behaviour is still runtime Python (solution)."""

from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")


def as_ints(values: list[str]) -> list[int]:
    """Parse each string as an int. Invalid tokens raise ValueError."""
    return [int(value) for value in values]


def first(items: list[T]) -> T:
    """Return items[0], or raise ValueError if empty."""
    if not items:
        raise ValueError("empty")
    return items[0]
