"""@timed and @retry — decorators that execute code (solution)."""

from __future__ import annotations

import time
from collections.abc import Callable
from functools import wraps
from typing import TypeVar

T = TypeVar("T")


def timed(fn: Callable[..., T]) -> Callable[..., tuple[T, float]]:
    """Return (result, elapsed_seconds). Preserve fn.__name__ with wraps."""

    @wraps(fn)
    def wrapped(*args: object, **kwargs: object) -> tuple[T, float]:
        started = time.perf_counter()
        result = fn(*args, **kwargs)
        return result, time.perf_counter() - started

    return wrapped


def retry(times: int) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Retry the function up to `times` attempts on Exception, then re-raise."""

    def decorator(fn: Callable[..., T]) -> Callable[..., T]:
        @wraps(fn)
        def wrapped(*args: object, **kwargs: object) -> T:
            last: Exception | None = None
            for _ in range(times):
                try:
                    return fn(*args, **kwargs)
                except Exception as exc:
                    last = exc
            assert last is not None
            raise last

        return wrapped

    return decorator
