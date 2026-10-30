"""Greet + a safe tag helper (solution)."""

from __future__ import annotations


def greet(name: str, prefix: str = "Hello") -> str:
    """Return '<prefix>, <name>'."""
    return f"{prefix}, {name}"


def add_tag(tag: str, tags: list[str] | None = None) -> list[str]:
    """Return a new list: the given tags (or empty) plus tag at the end.

    Must not reuse a default list between calls. Must not mutate the input list.
    """
    collected = [] if tags is None else list(tags)
    collected.append(tag)
    return collected
