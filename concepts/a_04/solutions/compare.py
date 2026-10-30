"""Guided: Jaccard overlap of owned vs hosted hit ids."""

from __future__ import annotations

from course_kit.hosted import overlap_rate as _overlap


def overlap_rate(own_ids: list[str], hosted_ids: list[str]) -> float:
    """Jaccard. Empty either side → 0.0."""
    return _overlap(own_ids, hosted_ids)
