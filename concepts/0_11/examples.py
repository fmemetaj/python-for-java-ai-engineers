"""list, dict, set, tuple — the four everyday collections."""

from __future__ import annotations


def count_levels(levels: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for level in levels:
        counts[level] = counts.get(level, 0) + 1
    return counts


def unique_in_order(items: list[str]) -> list[str]:
    return list(dict.fromkeys(items))


def pair_as_tuple(level: str, count: int) -> tuple[str, int]:
    return (level, count)


assert count_levels(["INFO", "ERROR", "INFO"]) == {"INFO": 2, "ERROR": 1}
assert unique_in_order(["INFO", "ERROR", "INFO"]) == ["INFO", "ERROR"]
assert pair_as_tuple("ERROR", 1) == ("ERROR", 1)
print("0.11 examples ok")
