"""Retry policy: 429 and 5xx, with exponential backoff."""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


class TransientError(Exception):
    pass


def should_retry(status_code: int) -> bool:
    """True for 429 and 5xx; False for other 4xx."""
    raise NotImplementedError


def backoff_seconds(attempt: int, base: float) -> float:
    """Zero-based attempt: 0 -> base, 1 -> 2*base, 2 -> 4*base."""
    raise NotImplementedError


def run_with_retry(
    fn: Callable[[], T],
    *,
    attempts: int,
    sleeper: Callable[[float], None],
    base_delay: float = 0.05,
) -> T:
    """Call fn until it succeeds or attempts are exhausted. Sleep on TransientError."""
    raise NotImplementedError
