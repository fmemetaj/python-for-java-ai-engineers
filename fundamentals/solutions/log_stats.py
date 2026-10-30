"""Typed log-file analyzer for Module 0A (solution)."""

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
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None
    level, _, message = stripped.partition(" ")
    if not _:
        return None
    return LogLine(level=level, message=message, raw=stripped)


def iter_logs(path: Path) -> Iterator[LogLine]:
    """Yield parsed lines lazily. Open the file as UTF-8."""
    with path.open(encoding="utf-8") as handle:
        for raw in handle:
            parsed = parse_line(raw)
            if parsed is not None:
                yield parsed


def count_by_level(path: Path) -> dict[str, int]:
    """Count occurrences of each level, first-seen order."""
    counts: dict[str, int] = {}
    for entry in iter_logs(path):
        counts[entry.level] = counts.get(entry.level, 0) + 1
    return counts


def messages_for_level(path: Path, level: str) -> list[str]:
    """Collect messages at the given level, in file order."""
    return [entry.message for entry in iter_logs(path) if entry.level == level]


def top_levels(path: Path, n: int = 3) -> list[tuple[str, int]]:
    """Return the n most common (level, count) pairs, ties broken by first-seen."""
    counts = count_by_level(path)
    ranked = sorted(counts.items(), key=lambda item: (-item[1], list(counts).index(item[0])))
    return ranked[:n]
