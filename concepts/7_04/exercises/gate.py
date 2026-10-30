"""Open: the capstone CI bar."""

from __future__ import annotations


def meets_capstone_bar(total: int, passed: int, min_cases: int = 30) -> bool:
    """True when total >= min_cases and every case passed. Reject bad counts."""
    raise NotImplementedError
