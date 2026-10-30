"""TTL response cache and timeout helpers. Java analog: Caffeine / @Cacheable.

``asyncio.gather`` is cooperative concurrent I/O (Module 0.29), not a thread
pool and not CPU parallelism. Timeouts are deadlines, like httpx
``timeout=`` / WebClient ``responseTimeout``.

This cache is in-process. It is not Redis. Tests inject ``clock``.
"""

from __future__ import annotations

import asyncio
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any, TypeVar

T = TypeVar("T")


@dataclass
class CacheEntry:
    value: Any
    expires_at: float


class TtlCache:
    """String-key TTL map. Expired entries are treated as misses."""

    def __init__(self, clock: Callable[[], float] | None = None) -> None:
        self._clock = clock or time.monotonic
        self._store: dict[str, CacheEntry] = {}

    def get(self, key: str) -> Any | None:
        entry = self._store.get(key)
        if entry is None:
            return None
        if entry.expires_at <= self._clock():
            del self._store[key]
            return None
        return entry.value

    def set(self, key: str, value: Any, ttl: float) -> None:
        if ttl < 0:
            raise ValueError("ttl must be >= 0")
        self._store[key] = CacheEntry(value=value, expires_at=self._clock() + ttl)

    def cache_get(
        self,
        key: str,
        compute: Callable[[], T],
        *,
        ttl: float,
    ) -> tuple[T, bool]:
        """Return (value, hit). On miss, call compute() and store."""
        cached = self.get(key)
        if cached is not None:
            return cached, True
        value = compute()
        self.set(key, value, ttl)
        return value, False


def is_timeout(elapsed: float, limit: float) -> bool:
    if elapsed < 0 or limit < 0:
        raise ValueError("elapsed and limit must be >= 0")
    return elapsed >= limit


async def gather_in_order(awaitables: Sequence[Any]) -> list[Any]:
    """``asyncio.gather`` preserving input order. Cooperative I/O, not threads."""
    return list(await asyncio.gather(*awaitables))


__all__ = ["CacheEntry", "TtlCache", "gather_in_order", "is_timeout"]
