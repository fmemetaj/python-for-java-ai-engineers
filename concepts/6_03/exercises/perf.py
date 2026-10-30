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
    raise NotImplementedError


def is_timeout(elapsed: float, limit: float) -> bool:
    """True when elapsed is at least limit."""
    raise NotImplementedError


def merge_in_order(results: Sequence[T]) -> list[T]:
    """Return a new list with the same order (gather analog)."""
    raise NotImplementedError
