"""Working memory with a token budget. Offline; no network."""

from __future__ import annotations

from course_kit.agent import AgentMemory
from course_kit.llm.tokens import estimate_tokens

# Example 1 — add an observation.
memory = AgentMemory(budget_tokens=80)
item = memory.add("observation", "search_docs: refunds page")
assert item.role == "observation"
assert item.tokens == estimate_tokens("search_docs: refunds page")

# Example 2 — pin the incident; it survives trim.
memory.add("user", "POST /payments/{id}/refunds returns 500 after capture", pinned=True)
assert any(entry.pinned for entry in memory.items)

# Example 3 — oldest unpinned drops first.
tight = AgentMemory(budget_tokens=20)
tight.add("user", "keep-me", pinned=True)
tight.add("observation", "alpha-alpha-alpha-alpha")
tight.add("observation", "beta-beta-beta-beta-beta")
roles = [entry.role for entry in tight.items]
assert "user" in roles
assert tight.used_tokens <= tight.budget_tokens or all(entry.pinned for entry in tight.items)

# Example 4 — scratchpad is shorter than dumping JSON.
notes = AgentMemory(budget_tokens=400)
notes.add("observation", "NPE in RefundService after capture")
notes.add("observation", "only captured payments can be refunded")
summary = notes.scratchpad(max_chars=40)
assert len(summary) <= 40
assert "NPE" in summary or "captured" in summary

# Example 5 — as_context is what the loop prepends to instructions.
ctx = notes.as_context()
assert "observation:" in ctx

print("5.3 examples ok")
