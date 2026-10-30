"""Cost per 100 requests from FakeLLM usage × pricing.yaml."""

from __future__ import annotations

from docsdesk.portfolio import build_cost_report, cost_per_n, cost_report_fields

# Example 1 — arithmetic.
assert cost_per_n(0.00004, 100) == 0.004

# Example 2 — required keys.
for key in ("usd_per_100", "pricing_source", "pricing_retrieved", "assumptions"):
    assert key in cost_report_fields()

# Example 3 — a real sample ask, still fake.
report = build_cost_report(requests=100)
assert report.requests == 100
assert report.provider == "fake"
assert report.usd_per_100 == cost_per_n(report.usd_per_request, 100)
assert "pricing" in report.pricing_source
assert any("Assistants" in line for line in report.assumptions)

# Example 4 — dated source, not a hard-coded README dollar.
assert report.pricing_retrieved

print(report.summary())
print("7.5 examples ok")
