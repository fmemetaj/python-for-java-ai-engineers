"""LEGB, no block scope, closures, and nonlocal."""

from __future__ import annotations

from collections.abc import Callable


def visible_after_if(flag: bool) -> str:
    if flag:
        label = "on"
    else:
        label = "off"
    return label


def make_counter(start: int = 0) -> Callable[[], int]:
    n = start

    def inc() -> int:
        nonlocal n
        n += 1
        return n

    return inc


assert visible_after_if(True) == "on"
assert visible_after_if(False) == "off"
counter = make_counter(10)
assert counter() == 11
assert counter() == 12
print("0.9 examples ok")
