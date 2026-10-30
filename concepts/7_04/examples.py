"""Capstone eval bundle ≥30 cases. Offline FakeLLM."""

from __future__ import annotations

from docsdesk.portfolio import (
    MIN_CAPSTONE_CASES,
    capstone_gate_ok,
    load_m7_manifest,
    meets_capstone_bar,
    run_v1_eval,
)

# Example 1 — the committed manifest refuses a bar below 30.
manifest = load_m7_manifest()
assert int(manifest["min_cases"]) >= MIN_CAPSTONE_CASES

# Example 2 — 29 perfect cases still miss the rubric.
assert meets_capstone_bar(29, 29) is False
assert meets_capstone_bar(44, 44) is True
assert meets_capstone_bar(44, 43) is False

# Example 3 — the real harness is fake-only and prefixes suite ids.
report = run_v1_eval(provider="fake")
assert report.total >= MIN_CAPSTONE_CASES
assert report.failed == 0
assert capstone_gate_ok(report) is True
assert any(item.id.startswith("m3:") for item in report.results)
assert any(item.id.startswith("m4:") for item in report.results)
assert any(item.id.startswith("inj:") for item in report.results)

# Example 4 — a live provider is opt-in and not this gate.
# (the harness raises RuntimeError; we do not call it here)

print(report.summary())
print("7.4 examples ok")
