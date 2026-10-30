"""Closures and the lack of block scope."""

from __future__ import annotations

from collections.abc import Callable


def make_counter(start: int = 0) -> Callable[[], int]:
    """Return a function that increments and returns an enclosed integer."""
    raise NotImplementedError


def visible_after_if(flag: bool) -> str:
    """Assign 'on' or 'off' inside if/else and return that name afterwards."""
    raise NotImplementedError
