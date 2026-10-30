"""TTL cache, timeouts, ordered merge."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any, TypeVar

T = TypeVar("T")


def cache_get(
    store: dict[str, tuple[Any, float]],
    key: str,
    compute: Callable[[], T],
    *,
    now: float,
    ttl: float,
) -> tuple[T, bool]:
    """Return (value, hit). Store values as (value, expires_at). Expired keys miss."""
    entry = store.get(key)
    if entry is not None:
        value, expires_at = entry
        if expires_at > now:
            return value, True
        del store[key]
    value = compute()
    store[key] = (value, now + ttl)
    return value, False


def is_timeout(elapsed: float, limit: float) -> bool:
    """True when elapsed is at least limit."""
    if elapsed < 0 or limit < 0:
        raise ValueError("elapsed and limit must be >= 0")
    return elapsed >= limit


def merge_in_order(results: Sequence[T]) -> list[T]:
    """Return a new list with the same order (gather analog)."""
    return list(results)
