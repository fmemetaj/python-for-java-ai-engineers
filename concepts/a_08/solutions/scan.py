"""Guided: find sunset API strings."""

from __future__ import annotations

from course_kit.upgrade import ScanFinding, scan_source, sunset_free


def findings(source: str) -> list[ScanFinding]:
    """Return ScanFinding rows for sunset / removed helpers."""
    return scan_source(source)


def is_clean(source: str) -> bool:
    """True when findings(source) is empty."""
    return sunset_free(source)
