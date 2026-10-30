"""Simulate notebook kernel state without starting Jupyter."""

from __future__ import annotations


def last_value(assignments: list[tuple[str, object]], name: str) -> object:
    current: dict[str, object] = {}
    for key, value in assignments:
        current[key] = value
    return current[name]


def missing_after_partial_run(defined: list[str], referenced: str) -> bool:
    return referenced not in set(defined)


# Example 1: shared namespace, last write wins
assert last_value([("count", 1), ("count", 2)], "count") == 2

# Example 2: a later cell can read an earlier name
assert last_value([("tickets", ["login"]), ("n", 1)], "tickets") == ["login"]

# Example 3: skip the cell that defined client → missing
assert missing_after_partial_run(["tickets"], "client") is True
assert missing_after_partial_run(["tickets", "client"], "client") is False

print("0.2 examples ok")
