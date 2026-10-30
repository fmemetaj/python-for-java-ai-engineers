"""Lazy error-line streaming (solution)."""

from __future__ import annotations

from collections.abc import Iterable, Iterator


def iter_errors(lines: Iterable[str]) -> Iterator[str]:
    """Yield lines that start with ERROR, in order, without building a list."""
    for line in lines:
        if line.startswith("ERROR"):
            yield line


def take(n: int, items: Iterable[object]) -> Iterator[object]:
    """Yield the first n items, then stop."""
    for index, item in enumerate(items):
        if index >= n:
            return
        yield item


def replay_count(items: Iterable[object]) -> int:
    """Iterate items once, then return how many items a second pass produces."""
    iterator = iter(items)
    list(iterator)
    return sum(1 for _ in iterator)
