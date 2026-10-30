"""Guided: judge pass bar and calibration agreement."""

from __future__ import annotations

from collections.abc import Sequence


def verdict_passes(score: int, threshold: int) -> bool:
    """True when score is at least threshold."""
    if threshold < 1:
        raise ValueError("threshold must be >= 1")
    return score >= threshold


def agreement_rate(predicted: Sequence[bool], labeled: Sequence[bool]) -> float:
    """Fraction of matching booleans. Sequences must be the same non-empty length."""
    if len(predicted) != len(labeled) or not predicted:
        raise ValueError("predicted and labeled must be the same non-empty length")
    hits = sum(pred is label for pred, label in zip(predicted, labeled, strict=True))
    return hits / len(predicted)
