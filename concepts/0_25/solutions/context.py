"""Context managers that time a block and open UTF-8 text (solution)."""

from __future__ import annotations

import time
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import TextIO


@contextmanager
def timed_block() -> Iterator[dict[str, float]]:
    """Yield a dict; on exit set dict['seconds'] to elapsed wall time."""
    started = time.perf_counter()
    data: dict[str, float] = {}
    try:
        yield data
    finally:
        data["seconds"] = time.perf_counter() - started


class Utf8File:
    def __init__(self, path: Path) -> None:
        self.path = path
        self._handle: TextIO | None = None

    def __enter__(self) -> TextIO:
        """Open the path for read with encoding='utf-8'."""
        self._handle = self.path.open(encoding="utf-8")
        return self._handle

    def __exit__(self, *args: object) -> None:
        """Close the handle if it was opened."""
        if self._handle is not None:
            self._handle.close()
            self._handle = None
