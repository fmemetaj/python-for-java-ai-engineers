"""Context managers that time a block and open UTF-8 text."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import TextIO


@contextmanager
def timed_block() -> Iterator[dict[str, float]]:
    """Yield a dict; on exit set dict['seconds'] to elapsed wall time."""
    raise NotImplementedError
    yield {}


class Utf8File:
    def __init__(self, path: Path) -> None:
        self.path = path
        self._handle: TextIO | None = None

    def __enter__(self) -> TextIO:
        """Open the path for read with encoding='utf-8'."""
        raise NotImplementedError

    def __exit__(self, *args: object) -> None:
        """Close the handle if it was opened."""
        raise NotImplementedError
