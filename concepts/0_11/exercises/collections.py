"""Aggregate log levels the way DocsDesk will."""


def count_levels(levels: list[str]) -> dict[str, int]:
    """Return how many times each level appears, first-seen key order."""
    raise NotImplementedError


def unique_in_order(items: list[str]) -> list[str]:
    """Return unique items, keeping the first occurrence of each."""
    raise NotImplementedError


def pair_as_tuple(level: str, count: int) -> tuple[str, int]:
    """Return an immutable (level, count) row."""
    raise NotImplementedError
