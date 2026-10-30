"""Open exercise: run a list of cases and report live rates without a threshold."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any


def run_harness(
    cases: Sequence[dict[str, Any]],
    grader: Callable[[dict[str, Any]], bool],
) -> dict[str, int]:
    """Return passed/failed/total for a golden set (must not crash on a bad case)."""
    passed = 0
    failed = 0
    for case in cases:
        try:
            ok = grader(case)
        except Exception:
            ok = False
        if ok:
            passed += 1
        else:
            failed += 1
    return {"passed": passed, "failed": failed, "total": len(cases)}


def live_rate_line(passed: int, total: int) -> str:
    """Report a live pass rate. Must include 'no threshold claimed'."""
    return f"live pass rate {passed}/{total} (no threshold claimed)"
