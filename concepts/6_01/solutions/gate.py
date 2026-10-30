"""Open: CI gate and injected regression."""

from __future__ import annotations

from typing import Any


def gate_ok(passed: int, total: int, min_pass_rate: float) -> bool:
    """True when passed/total is at least min_pass_rate. total must be > 0."""
    if not 0.0 <= min_pass_rate <= 1.0:
        raise ValueError("min_pass_rate must be in [0, 1]")
    if total <= 0:
        return False
    return (passed / total) >= min_pass_rate


def inject_wrong_answer(
    cases: list[dict[str, Any]],
    case_id: str,
    expected_answer: str,
) -> list[dict[str, Any]]:
    """Return a copy where the matching case has a new expected_answer."""
    out: list[dict[str, Any]] = []
    found = False
    for case in cases:
        row = dict(case)
        if row.get("id") == case_id:
            row["expected_answer"] = expected_answer
            found = True
        out.append(row)
    if not found:
        raise KeyError(f"no eval case {case_id!r}")
    return out
