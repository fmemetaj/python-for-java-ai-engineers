"""Guided: find sunset API strings."""

from __future__ import annotations

from course_kit.upgrade import ScanFinding


def findings(source: str) -> list[ScanFinding]:
    """Return ScanFinding rows for sunset / removed helpers."""
    raise NotImplementedError


def is_clean(source: str) -> bool:
    """True when findings(source) is empty."""
    raise NotImplementedError
