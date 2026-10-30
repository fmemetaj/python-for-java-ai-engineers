"""Portfolio README sections and the five-minute demo. Offline."""

from __future__ import annotations

from docsdesk.portfolio import demo_minutes, print_portfolio, readme_sections, self_assessment_items
from docsdesk.v1 import DocsDeskV1

# Example 1 — hiring-manager sections.
sections = readme_sections()
assert "eval report" in sections
assert "threat model" in sections
assert "limitations" in sections

# Example 2 — five minutes, not a webinar.
assert demo_minutes() == 5

# Example 3 — self-assessment mentions the rubric.
blob = " ".join(self_assessment_items()).lower()
assert "30" in blob
assert "citation" in blob

# Example 4 — the actual demo path (simulated).
with DocsDeskV1(approved=True) as desk:
    turns = desk.demo()
assert len(turns) == 2
assert turns[0].citations
assert turns[1].status == "done"

print_portfolio()
print("7.7 examples ok")
