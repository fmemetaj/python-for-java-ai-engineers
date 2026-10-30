"""Aggregate log levels the way DocsDesk will (solution)."""


def count_levels(levels: list[str]) -> dict[str, int]:
    """Return how many times each level appears, first-seen key order."""
    counts: dict[str, int] = {}
    for level in levels:
        counts[level] = counts.get(level, 0) + 1
    return counts


def unique_in_order(items: list[str]) -> list[str]:
    """Return unique items, keeping the first occurrence of each."""
    return list(dict.fromkeys(items))


def pair_as_tuple(level: str, count: int) -> tuple[str, int]:
    """Return an immutable (level, count) row."""
    return (level, count)
