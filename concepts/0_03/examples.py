"""Rebinding versus in-place mutation."""

from __future__ import annotations


def after_rebind(original: list[int]) -> tuple[list[int], list[int]]:
    alias = original
    rebound = [0]
    original = rebound
    return alias, original


def after_mutate(original: list[int]) -> tuple[list[int], list[int]]:
    alias = original
    original.append(99)
    return alias, original


alias, rebound = after_rebind([1, 2])
assert alias == [1, 2]
assert rebound == [0]

alias, mutated = after_mutate([1, 2])
assert alias == [1, 2, 99]
assert mutated is alias

print("0.3 examples ok")
