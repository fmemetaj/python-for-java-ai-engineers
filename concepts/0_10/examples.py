"""Functions as values, plus a one-expression lambda."""

from __future__ import annotations

from collections.abc import Callable


def apply_each(fn: Callable[[int], int], values: list[int]) -> list[int]:
    return [fn(value) for value in values]


def sort_by_length(words: list[str]) -> list[str]:
    return sorted(words, key=len)


def make_adder(n: int) -> Callable[[int], int]:
    return lambda value: value + n


assert apply_each(lambda x: x * 2, [1, 2, 3]) == [2, 4, 6]
assert sort_by_length(["login", "api", "ok"]) == ["ok", "api", "login"]
assert make_adder(2)(5) == 7
print("0.10 examples ok")
