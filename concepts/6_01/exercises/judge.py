"""Guided: judge pass bar and calibration agreement."""

from __future__ import annotations

from collections.abc import Sequence


def verdict_passes(score: int, threshold: int) -> bool:
    """True when score is at least threshold."""
    raise NotImplementedError


def agreement_rate(predicted: Sequence[bool], labeled: Sequence[bool]) -> float:
    """Fraction of matching booleans. Sequences must be the same non-empty length."""
    raise NotImplementedError
