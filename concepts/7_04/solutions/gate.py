"""Open: the capstone CI bar."""

from __future__ import annotations


def meets_capstone_bar(total: int, passed: int, min_cases: int = 30) -> bool:
    """True when total >= min_cases and every case passed. Reject bad counts."""
    if min_cases < 1:
        raise ValueError("min_cases must be >= 1")
    if total < 0 or passed < 0:
        raise ValueError("counts must be >= 0")
    if passed > total:
        raise ValueError("passed cannot exceed total")
    return total >= min_cases and passed == total
