"""ThreadPoolExecutor preserving result order (solution)."""

from __future__ import annotations

from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from typing import TypeVar

T = TypeVar("T")
U = TypeVar("U")


def run_parallel(fn: Callable[[T], U], items: list[T], max_workers: int = 4) -> list[U]:
    """Map fn over items with ThreadPoolExecutor. Preserve input order."""
    if not items:
        return []
    workers = max(1, min(max_workers, len(items)))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(fn, items))
