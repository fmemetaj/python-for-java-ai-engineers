"""Open exercise: run a list of cases and report live rates without a threshold."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any


def run_harness(
    cases: Sequence[dict[str, Any]],
    grader: Callable[[dict[str, Any]], bool],
) -> dict[str, int]:
    """Return passed/failed/total for a golden set (must not crash on a bad case)."""
    raise NotImplementedError


def live_rate_line(passed: int, total: int) -> str:
    """Report a live pass rate. Must include 'no threshold claimed'."""
    raise NotImplementedError
