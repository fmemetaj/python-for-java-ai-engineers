"""Owned RAG vs hosted file_search. Offline canned hits."""

from __future__ import annotations

from course_kit.hosted import choose_stack, overlap_rate
from docsdesk.hosted import compare_retrieve

# Example 1 — Jaccard of disjoint ids is 0.
assert overlap_rate(["refunds:0"], ["hosted-refund"]) == 0.0

# Example 2 — eval-able owned pipeline wins.
assert (
    choose_stack(
        own_recall=0.8,
        hosted_available=True,
        can_export=True,
        can_eval=True,
        overlap=0.1,
    ).choice
    == "own"
)

# Example 3 — no eval yet → hosted is a prototype only.
assert (
    choose_stack(
        own_recall=0.0,
        hosted_available=True,
        can_export=False,
        can_eval=False,
        overlap=0.0,
    ).choice
    == "hosted"
)

# Example 4 — DocsDesk comparison stays on FakeEmbedder.
comparison = compare_retrieve("How do I refund a captured payment?")
assert comparison.decision.choice == "own"
assert comparison.hosted_ids

# Example 5 — hosted flags say vendor chunking is not CI-honest.
flags = comparison.record["flags"]
assert isinstance(flags, dict)
assert flags["ci_honest"] is False
print(comparison.decision.reason)
print("A.4 examples ok")
