"""Guided: merge suite counts into one report."""

from __future__ import annotations


def merge_counts(parts: list[tuple[int, int]]) -> tuple[int, int]:
    """Sum (passed, total) pairs. Ignore nothing; empty parts → (0, 0)."""
    passed = sum(row[0] for row in parts)
    total = sum(row[1] for row in parts)
    return passed, total
