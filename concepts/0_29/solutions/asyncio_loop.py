"""Cooperative concurrent I/O — not CPU parallelism (solution)."""

from __future__ import annotations

import asyncio


async def fake_lookup(name: str) -> str:
    """Yield to the event loop, then return name."""
    await asyncio.sleep(0)
    return name


async def gather_names(names: list[str]) -> list[str]:
    """Run fake_lookup concurrently; return results in the same order as names."""
    results = await asyncio.gather(*[fake_lookup(name) for name in names])
    return list(results)


async def max_concurrent(count: int) -> int:
    """Start `count` tasks that overlap. Return how many ran at once (peak)."""
    running = 0
    peak = 0
    gate = asyncio.Event()

    async def one() -> None:
        nonlocal running, peak
        running += 1
        peak = max(peak, running)
        if running == count:
            gate.set()
        await gate.wait()
        running -= 1

    await asyncio.gather(*[one() for _ in range(count)])
    return peak
