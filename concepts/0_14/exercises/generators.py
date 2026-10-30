"""Lazy error-line streaming."""

from __future__ import annotations

from collections.abc import Iterable, Iterator


def iter_errors(lines: Iterable[str]) -> Iterator[str]:
    """Yield lines that start with ERROR, in order, without building a list."""
    raise NotImplementedError


def take(n: int, items: Iterable[object]) -> Iterator[object]:
    """Yield the first n items, then stop."""
    raise NotImplementedError


def replay_count(items: Iterable[object]) -> int:
    """Iterate items once, then return how many items a second pass produces."""
    raise NotImplementedError
