"""Capstone briefs and required artifacts. Offline, no network."""

from __future__ import annotations

from docsdesk.portfolio import choose_brief, required_artifacts

# Example 1 — three original briefs.
own = choose_brief("own-repo")
assert own["id"] == "own-repo"
assert own["write_tools"] is False

# Example 2 — PR review may write, but only after approval (later lesson).
review = choose_brief("pr-review")
assert review["write_tools"] is True

# Example 3 — log triage reuses the Module 5 loop.
triage = choose_brief("log-triage")
assert "log" in triage["corpus"].lower()

# Example 4 — unknown names fail closed.
try:
    choose_brief("secret-saas")
except KeyError:
    pass
else:
    raise AssertionError("unknown briefs must raise")

# Example 5 — the rubric's six artifacts.
names = required_artifacts()
assert "eval report" in names
assert "threat model" in names
assert "demo" in names

print("briefs", own["id"], review["id"], triage["id"])
print("7.1 examples ok")
