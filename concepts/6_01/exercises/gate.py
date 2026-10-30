"""Open: CI gate and injected regression."""

from __future__ import annotations

from typing import Any


def gate_ok(passed: int, total: int, min_pass_rate: float) -> bool:
    """True when passed/total is at least min_pass_rate. total must be > 0."""
    raise NotImplementedError


def inject_wrong_answer(
    cases: list[dict[str, Any]],
    case_id: str,
    expected_answer: str,
) -> list[dict[str, Any]]:
    """Return a copy where the matching case has a new expected_answer."""
    raise NotImplementedError
