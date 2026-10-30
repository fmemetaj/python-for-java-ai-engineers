"""Closures and the lack of block scope (solution)."""

from __future__ import annotations

from collections.abc import Callable


def make_counter(start: int = 0) -> Callable[[], int]:
    """Return a function that increments and returns an enclosed integer."""
    n = start

    def inc() -> int:
        nonlocal n
        n += 1
        return n

    return inc


def visible_after_if(flag: bool) -> str:
    """Assign 'on' or 'off' inside if/else and return that name afterwards."""
    if flag:
        label = "on"
    else:
        label = "off"
    return label
