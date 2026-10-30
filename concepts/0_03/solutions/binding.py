"""Rebind vs mutate (solution)."""


def after_rebind(original: list[int]) -> tuple[list[int], list[int]]:
    """Bind alias to original, then rebind original to [0]. Return (alias, original)."""
    alias = original
    original = [0]
    return alias, original


def after_mutate(original: list[int]) -> tuple[list[int], list[int]]:
    """Bind alias to original, append 99 to original. Return (alias, original)."""
    alias = original
    original.append(99)
    return alias, original
