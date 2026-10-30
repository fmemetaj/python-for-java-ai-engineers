"""Rewrite a Java Stream filter+map three ways (solution)."""

from __future__ import annotations

from collections.abc import Iterator


def high_priority_ids(tickets: list[dict[str, str | int]]) -> list[int]:
    """Comprehension: ids of tickets whose priority is high."""
    return [int(ticket["id"]) for ticket in tickets if ticket["priority"] == "high"]


def high_priority_ids_loop(tickets: list[dict[str, str | int]]) -> list[int]:
    """The same result, written as an explicit for-loop."""
    ids: list[int] = []
    for ticket in tickets:
        if ticket["priority"] == "high":
            ids.append(int(ticket["id"]))
    return ids


def high_priority_ids_gen(tickets: list[dict[str, str | int]]) -> Iterator[int]:
    """The same filter/map, yielded one id at a time."""
    for ticket in tickets:
        if ticket["priority"] == "high":
            yield int(ticket["id"])
