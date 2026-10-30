"""Module 6 evals: judge + CI gate + prompt-injection suite. Offline FakeLLM."""

from __future__ import annotations

import json
import os
from typing import Any

from course_kit.loader import repo_root

from .evals import CaseResult, EvalReport, exact_match, load_eval_cases, run_docsdesk_eval
from .gate import eval_gate, inject_regression
from .judge import judge_answer, scripted_judge
from .security import (
    looks_like_injection,
    output_leaks_secret,
    redact_secrets,
    strip_injected_instructions,
)

M6_EVAL_FILE = "data/evals/docsdesk_m6.json"
INJECTION_FILE = "data/evals/docsdesk_injection.json"


def load_json_cases(relative: str) -> list[dict[str, Any]]:
    path = repo_root() / relative
    payload = json.loads(path.read_text(encoding="utf-8"))
    cases = payload["cases"]
    if not isinstance(cases, list) or not cases:
        raise ValueError(f"{relative} must contain a non-empty cases list")
    return cases


def run_m6_eval(*, provider: str | None = None) -> EvalReport:
    """Golden + judge cases. Graded CI uses fake only."""
    name = (provider or os.environ.get("LLM_PROVIDER") or "fake").strip().lower() or "fake"
    if name != "fake":
        raise RuntimeError(
            "Live eval is optional. Keep LLM_PROVIDER=fake for graded work. "
            "No pass threshold is claimed for a live judge."
        )
    cases = load_json_cases(M6_EVAL_FILE)
    golden = [case for case in cases if case.get("check") != "judge"]
    judge_cases = [case for case in cases if case.get("check") == "judge"]
    report = run_docsdesk_eval(provider="fake", cases=golden) if golden else EvalReport(0, 0, 0)
    judge = scripted_judge()
    extra: list[CaseResult] = []
    for case in judge_cases:
        case_id = str(case["id"])
        try:
            verdict = judge_answer(
                str(case["answer"]), client=judge, threshold=int(case["min_score"])
            )
            extra.append(CaseResult(case_id, verdict.passed, "judge", verdict.rationale))
        except Exception as exc:  # noqa: BLE001 — harness must not crash
            extra.append(CaseResult(case_id, False, "judge", f"{type(exc).__name__}: {exc}"))
    results = list(report.results) + extra
    passed = sum(1 for item in results if item.passed)
    return EvalReport(
        passed=passed,
        failed=len(results) - passed,
        total=len(results),
        results=results,
        provider="fake",
    )


def run_injection_suite() -> EvalReport:
    """Offline injection fixtures. Pass = detector/redactor behaved as expected."""
    cases = load_json_cases(INJECTION_FILE)
    results: list[CaseResult] = []
    for case in cases:
        case_id = str(case["id"])
        kind = str(case["kind"])
        try:
            ok = _grade_injection(case)
        except Exception as exc:  # noqa: BLE001
            ok = False
            results.append(CaseResult(case_id, False, kind, f"{type(exc).__name__}: {exc}"))
            continue
        results.append(CaseResult(case_id, ok, kind))
    passed = sum(1 for item in results if item.passed)
    return EvalReport(
        passed=passed,
        failed=len(results) - passed,
        total=len(results),
        results=results,
        provider="fake",
    )


def _grade_injection(case: dict[str, Any]) -> bool:
    kind = str(case["kind"])
    expect = str(case["expect"])
    if kind == "direct":
        blocked = looks_like_injection(str(case["prompt"]))
        return blocked if expect == "blocked" else not blocked
    if kind == "benign":
        return looks_like_injection(str(case["prompt"])) is False
    if kind == "leak":
        secrets = [str(item) for item in case["secrets"]]
        output = str(case["output"])
        redacted = redact_secrets(output, secrets)
        leaked = output_leaks_secret(redacted, secrets)
        return (not leaked) if expect == "redacted" else leaked
    if kind == "indirect":
        stripped = strip_injected_instructions(str(case["doc"]))
        return looks_like_injection(stripped) is False
    if kind == "tool":
        return looks_like_injection(str(case["prompt"])) is True
    raise ValueError(f"unknown injection kind {kind}")


def regression_gate_fails() -> bool:
    """True when mutating one golden expected answer makes eval_gate fail.

    This is the Module 6 acceptance: a CI eval gate fails on an injected
    regression. It uses the Module 3 exact-auth case and FakeLLM.
    """
    cases = load_eval_cases()
    mutated = inject_regression(cases, "exact-auth", "THIS_IS_A_REGRESSION")
    report = run_docsdesk_eval(provider="fake", cases=mutated)
    # Sanity: the unmutated set still has that case as exact match.
    assert not exact_match(
        "THIS_IS_A_REGRESSION", "Clients send a Bearer token. DocsDesk never logs the token."
    )
    return eval_gate(report, min_pass_rate=1.0) is False


__all__ = [
    "INJECTION_FILE",
    "M6_EVAL_FILE",
    "load_json_cases",
    "regression_gate_fails",
    "run_injection_suite",
    "run_m6_eval",
]
