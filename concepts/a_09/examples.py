"""Spend-capped smoke + sanitized fixtures. FakeLLM only."""

from __future__ import annotations

from course_kit.upgrade import SmokeCall, run_smoke, sanitize_record
from docsdesk.smoke import run_elective_smoke

# Example 1 — the third call would exceed $0.01.
report = run_smoke(
    [SmokeCall("a", 0.004), SmokeCall("b", 0.004), SmokeCall("c", 0.004)],
    0.01,
)
assert report.skipped == ("c",)

# Example 2 — DocsDesk smoke uses FakeLLM usage → USD from pricing.yaml.
elective = run_elective_smoke(cap_usd=0.01)
assert elective.report.within_budget is True
assert elective.fixture["provider"] == "fake"

# Example 3 — recorded JSON must not keep keys.
cleaned = sanitize_record({"key": "sk-abcdefghijklmnop"})
assert cleaned["key"] == "***"

# Example 4 — Bearer headers go too.
cleaned = sanitize_record({"Authorization": "Bearer abc.def"})
assert "***" in cleaned["Authorization"]

# Example 5 — the fake cannot teach a real 429; the cap is the drill.
print(elective.summary())
print("A.9 examples ok")
