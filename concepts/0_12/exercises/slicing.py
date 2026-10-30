"""Slice windows and unpack the head of a sequence."""


def tail(seq: list[int], n: int) -> list[int]:
    """Return the last n items (copy). Empty list if n <= 0."""
    raise NotImplementedError


def every_other(seq: list[int]) -> list[int]:
    """Return items at indexes 0, 2, 4, ... (a copy)."""
    raise NotImplementedError


def split_head(seq: list[int]) -> tuple[int, list[int]]:
    """Return (first item, remaining items as a new list). seq is non-empty."""
    raise NotImplementedError
