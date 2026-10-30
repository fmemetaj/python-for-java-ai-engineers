"""Eval strategy: judge, calibration, CI gate, injected regression. Offline FakeLLM."""

from __future__ import annotations

from docsdesk.evals import exact_match, run_docsdesk_eval
from docsdesk.gate import eval_gate, inject_regression
from docsdesk.judge import agreement_rate, judge_answer, verdict_passes
from docsdesk.prod_eval import regression_gate_fails, run_m6_eval

# Example 1 — exact match stays for fixtures.
assert exact_match("Bearer token", "Bearer token") is True
assert exact_match("Bearer token", "bearer token") is False

# Example 2 — scripted judge scores the auth fixture at or above 4.
verdict = judge_answer("Clients send a Bearer token. DocsDesk never logs the token.")
assert verdict_passes(verdict.score, 4) is True
assert verdict.passed is True

# Example 3 — calibration is agreement with labels, not "the judge said so".
predicted = [True, True, False, True]
labeled = [True, False, False, True]
assert agreement_rate(predicted, labeled) == 0.75

# Example 4 — committed M6 set passes the fake gate.
report = run_m6_eval(provider="fake")
assert report.failed == 0
assert eval_gate(report, min_pass_rate=1.0) is True
assert "CI gate" in report.summary()

# Example 5 — mutating one expected answer turns the gate red.
assert regression_gate_fails() is True
mutated = inject_regression(
    [
        {
            "id": "exact-auth",
            "check": "exact",
            "prompt": "How do clients authenticate?",
            "expected_answer": "Clients send a Bearer token. DocsDesk never logs the token.",
        }
    ],
    "exact-auth",
    "WRONG",
)
assert mutated[0]["expected_answer"] == "WRONG"
baseline = run_docsdesk_eval(provider="fake")
assert eval_gate(baseline, min_pass_rate=1.0) is True

print(report.summary())
print("6.1 examples ok")
