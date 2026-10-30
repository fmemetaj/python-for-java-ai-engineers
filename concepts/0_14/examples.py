"""Generators pause; a second pass is empty."""

from __future__ import annotations

from collections.abc import Iterable, Iterator


def iter_errors(lines: Iterable[str]) -> Iterator[str]:
    for line in lines:
        if line.startswith("ERROR"):
            yield line


def take(n: int, items: Iterable[object]) -> Iterator[object]:
    for index, item in enumerate(items):
        if index >= n:
            return
        yield item


def replay_count(items: Iterable[object]) -> int:
    iterator = iter(items)
    list(iterator)
    return sum(1 for _ in iterator)


assert list(iter_errors(["INFO ok", "ERROR disk", "WARN x", "ERROR timeout"])) == [
    "ERROR disk",
    "ERROR timeout",
]
assert list(take(2, [10, 20, 30, 40])) == [10, 20]
assert replay_count(iter_errors(["ERROR a", "ERROR b"])) == 0
print("0.14 examples ok")
