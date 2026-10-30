"""Rebind vs mutate. Return (alias, current_original)."""


def after_rebind(original: list[int]) -> tuple[list[int], list[int]]:
    """Bind alias to original, then rebind original to [0]. Return (alias, original)."""
    raise NotImplementedError


def after_mutate(original: list[int]) -> tuple[list[int], list[int]]:
    """Bind alias to original, append 99 to original. Return (alias, original)."""
    raise NotImplementedError
