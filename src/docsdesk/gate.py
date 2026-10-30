"""CI eval gates. A frozen baseline fails the merge when a prompt regresses.

The gate is a number: ``passed / total >= min_pass_rate``. FakeLLM makes
``min_pass_rate=1.0`` honest. Live models report a rate and do **not** use
this function as a claimed threshold.

``inject_regression`` mutates a golden case so tests can prove the gate goes
red. That mutation is a test helper — it is not a production feature.
"""

from __future__ import annotations

from typing import Any

from .evals import EvalReport


def eval_gate(report: EvalReport, *, min_pass_rate: float = 1.0) -> bool:
    """True when the report meets the frozen pass-rate bar."""
    if not 0.0 <= min_pass_rate <= 1.0:
        raise ValueError("min_pass_rate must be in [0, 1]")
    if report.total <= 0:
        return False
    return (report.passed / report.total) >= min_pass_rate


def inject_regression(
    cases: list[dict[str, Any]],
    case_id: str,
    expected_answer: str,
) -> list[dict[str, Any]]:
    """Return a copy where one exact-match case expects the wrong string."""
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


__all__ = ["eval_gate", "inject_regression"]
