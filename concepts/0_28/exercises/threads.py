"""ThreadPoolExecutor preserving result order."""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")
U = TypeVar("U")


def run_parallel(fn: Callable[[T], U], items: list[T], max_workers: int = 4) -> list[U]:
    """Map fn over items with ThreadPoolExecutor. Preserve input order."""
    raise NotImplementedError
