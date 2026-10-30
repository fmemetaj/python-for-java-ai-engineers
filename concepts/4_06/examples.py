"""recall@k and groundedness. Offline gold labels."""

from __future__ import annotations

from docsdesk.retrieval_eval import groundedness_score, recall_at_k

# Example 1 — hit.
assert recall_at_k(["payments", "refunds"], ["refunds"], k=5) == 1.0

# Example 2 — miss.
assert recall_at_k(["payments", "errors"], ["PaymentController"], k=5) == 0.0

# Example 3 — partial.
assert recall_at_k(["refunds"], ["refunds", "payments"], k=5) == 0.5

# Example 4 — invented citation.
assert groundedness_score(["invented:9"], ["refunds:0"]) == 0.0
assert groundedness_score(["refunds:0"], ["refunds:0", "payments:1"]) == 1.0
assert groundedness_score([], ["refunds:0"]) == 0.0

# Example 5 — k cuts the list.
assert recall_at_k(["noise", "refunds"], ["refunds"], k=1) == 0.0

print("4.6 examples ok")
