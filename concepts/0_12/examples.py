"""Slicing copies; starred unpacking peels a sequence apart."""

from __future__ import annotations


def tail(seq: list[int], n: int) -> list[int]:
    if n <= 0:
        return []
    return seq[-n:]


def every_other(seq: list[int]) -> list[int]:
    return seq[::2]


def split_head(seq: list[int]) -> tuple[int, list[int]]:
    head, *rest = seq
    return head, rest


assert tail([10, 20, 30, 40], 2) == [30, 40]
assert every_other([10, 20, 30, 40]) == [10, 30]
assert split_head([10, 20, 30]) == (10, [20, 30])
copied = [1, 2][:]
copied.append(3)
assert copied == [1, 2, 3]
print("0.12 examples ok")
