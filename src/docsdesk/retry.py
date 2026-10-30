"""Retry with exponential backoff. Java analogy: Spring Retry / Resilience4j."""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


class TransientError(Exception):
    """HTTP 429 / 5xx or a timeout — worth retrying."""

    def __init__(self, message: str, *, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


def should_retry(status_code: int) -> bool:
    """Retry rate limits and server errors. Do not retry ordinary 4xx."""
    return status_code == 429 or status_code >= 500


def backoff_seconds(attempt: int, base: float) -> float:
    """attempt 0 → base, 1 → 2*base, 2 → 4*base. `attempt` is zero-based."""
    return base * (2**attempt)


def run_with_retry(
    fn: Callable[[], T],
    *,
    attempts: int,
    sleeper: Callable[[float], None],
    base_delay: float = 0.05,
) -> T:
    last: BaseException | None = None
    for attempt in range(attempts):
        try:
            return fn()
        except TransientError as exc:
            last = exc
            if attempt >= attempts - 1:
                raise
            sleeper(backoff_seconds(attempt, base_delay))
    assert last is not None
    raise last
