"""The same Stream pipeline as a comprehension, a loop, and a generator."""

from __future__ import annotations

from collections.abc import Iterator


def high_priority_ids(tickets: list[dict[str, str | int]]) -> list[int]:
    return [int(ticket["id"]) for ticket in tickets if ticket["priority"] == "high"]


def high_priority_ids_loop(tickets: list[dict[str, str | int]]) -> list[int]:
    ids: list[int] = []
    for ticket in tickets:
        if ticket["priority"] == "high":
            ids.append(int(ticket["id"]))
    return ids


def high_priority_ids_gen(tickets: list[dict[str, str | int]]) -> Iterator[int]:
    for ticket in tickets:
        if ticket["priority"] == "high":
            yield int(ticket["id"])


tickets = [
    {"id": 101, "priority": "high"},
    {"id": 102, "priority": "low"},
    {"id": 103, "priority": "high"},
]
assert high_priority_ids(tickets) == [101, 103]
assert high_priority_ids_loop(tickets) == [101, 103]
assert list(high_priority_ids_gen(tickets)) == [101, 103]
print("0.15 examples ok")
