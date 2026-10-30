"""Pass, sort with, and return functions."""

from __future__ import annotations

from collections.abc import Callable


def apply_each(fn: Callable[[int], int], values: list[int]) -> list[int]:
    """Return fn(value) for each value, in order."""
    raise NotImplementedError


def sort_by_length(words: list[str]) -> list[str]:
    """Return a new list of words sorted by increasing length."""
    raise NotImplementedError


def make_adder(n: int) -> Callable[[int], int]:
    """Return a function that adds n to its argument."""
    raise NotImplementedError
