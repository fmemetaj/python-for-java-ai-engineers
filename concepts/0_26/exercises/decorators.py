"""@timed and @retry — decorators that execute code."""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def timed(fn: Callable[..., T]) -> Callable[..., tuple[T, float]]:
    """Return (result, elapsed_seconds). Preserve fn.__name__ with wraps."""
    raise NotImplementedError


def retry(times: int) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Retry the function up to `times` attempts on Exception, then re-raise."""
    raise NotImplementedError
