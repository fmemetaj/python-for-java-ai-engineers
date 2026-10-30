"""Typed log-file analyzer for Module 0A (starter).

Fill this in after concepts 0.1–0.15. Grade with:

    uv run pytest fundamentals/test_log_stats.py
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LogLine:
    level: str
    message: str
    raw: str


def parse_line(line: str) -> LogLine | None:
    """Parse 'LEVEL message'. Return None for blanks and comments (#)."""
    raise NotImplementedError


def iter_logs(path: Path) -> Iterator[LogLine]:
    """Yield parsed lines lazily. Open the file as UTF-8."""
    raise NotImplementedError


def count_by_level(path: Path) -> dict[str, int]:
    """Count occurrences of each level, first-seen order."""
    raise NotImplementedError


def messages_for_level(path: Path, level: str) -> list[str]:
    """Collect messages at the given level, in file order."""
    raise NotImplementedError


def top_levels(path: Path, n: int = 3) -> list[tuple[str, int]]:
    """Return the n most common (level, count) pairs, ties broken by first-seen."""
    raise NotImplementedError
