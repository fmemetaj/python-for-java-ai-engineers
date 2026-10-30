"""Evals 101: exact, schema, rubric, 15-case harness. Offline FakeLLM."""

from __future__ import annotations

from docsdesk.evals import (
    exact_match,
    format_live_rate,
    rubric_contains,
    run_docsdesk_eval,
    schema_ok,
)
from docsdesk.models import Incident

# Example 1 — exact match is for fixtures, not live prose.
assert exact_match("Bearer", "Bearer") is True
assert exact_match("Bearer", "bearer") is False

# Example 2 — schema check: Pydantic, not isinstance.
payload = {
    "service": "auth",
    "severity": "high",
    "summary": "token validation failed for 12 requests",
    "timestamp": "2026-10-30T08:00:00Z",
}
assert schema_ok("Incident", payload) is True
assert Incident.model_validate(payload).service == "auth"

# Example 3 — rubric: required substrings (case-insensitive).
assert rubric_contains("Clients send a Bearer token.", ["bearer"]) is True

# Example 4 — the committed 15+ case set passes on fake.
report = run_docsdesk_eval(provider="fake")
assert report.total >= 15
assert report.failed == 0
assert "CI gate" in report.summary()

# Example 5 — live reporting has no pass bar.
line = format_live_rate(report.passed, report.total)
assert "no threshold claimed" in line

print(report.summary())
print("3.5 examples ok")
