"""Performance: TTL cache, timeouts, gather. Offline, no network."""

from __future__ import annotations

import asyncio

from docsdesk.cache import TtlCache, gather_in_order, is_timeout
from docsdesk.production import ProductionDesk

# Example 1 — miss then hit.
clock = {"t": 0.0}
cache = TtlCache(clock=lambda: clock["t"])
calls = {"n": 0}


def compute() -> str:
    calls["n"] += 1
    return "Bearer"


value, hit = cache.cache_get("auth", compute, ttl=10.0)
assert (value, hit, calls["n"]) == ("Bearer", False, 1)
value, hit = cache.cache_get("auth", compute, ttl=10.0)
assert (value, hit, calls["n"]) == ("Bearer", True, 1)

# Example 2 — TTL expiry is a miss.
clock["t"] = 11.0
value, hit = cache.cache_get("auth", compute, ttl=10.0)
assert hit is False
assert calls["n"] == 2

# Example 3 — timeout includes equality.
assert is_timeout(4.9, 5.0) is False
assert is_timeout(5.0, 5.0) is True


# Example 4 — gather preserves order (cooperative I/O, not threads).
async def _one() -> str:
    return "a"


async def _two() -> str:
    return "b"


assert asyncio.run(gather_in_order([_one(), _two()])) == ["a", "b"]

# Example 5 — ProductionDesk second ask is a cache hit.
with ProductionDesk() as desk:
    first = desk.ask("How do clients authenticate?")
    second = desk.ask("How do clients authenticate?")
assert first.cached is False
assert second.cached is True
assert second.cost_usd == 0.0
assert first.answer == second.answer

print("6.3 examples ok")
