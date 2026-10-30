"""Cooperative concurrent I/O — not CPU parallelism."""

from __future__ import annotations


async def fake_lookup(name: str) -> str:
    """Yield to the event loop, then return name."""
    raise NotImplementedError


async def gather_names(names: list[str]) -> list[str]:
    """Run fake_lookup concurrently; return results in the same order as names."""
    raise NotImplementedError


async def max_concurrent(count: int) -> int:
    """Start `count` tasks that overlap. Return how many ran at once (peak)."""
    raise NotImplementedError
