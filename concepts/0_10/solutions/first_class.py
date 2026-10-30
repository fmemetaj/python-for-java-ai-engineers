"""Pass, sort with, and return functions (solution)."""

from __future__ import annotations

from collections.abc import Callable


def apply_each(fn: Callable[[int], int], values: list[int]) -> list[int]:
    """Return fn(value) for each value, in order."""
    return [fn(value) for value in values]


def sort_by_length(words: list[str]) -> list[str]:
    """Return a new list of words sorted by increasing length."""
    return sorted(words, key=len)


def make_adder(n: int) -> Callable[[int], int]:
    """Return a function that adds n to its argument."""
    return lambda value: value + n
