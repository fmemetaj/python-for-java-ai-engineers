"""Fake hosted file_search loop. Two steps, then stop."""

from __future__ import annotations

from course_kit.hosted import RetrievalHit, next_hosted_turn

hits = [RetrievalHit("hosted-refund", "hosted:refunds.md", "POST /payments/{id}/refunds", 0.88)]

# Example 1 — step 0 is a tool call the platform would run.
tool = next_hosted_turn(0, "How do I refund?", hits)
assert tool.kind == "tool"
assert tool.call is not None and tool.call.call_id == "fs_1"

# Example 2 — step 1 is the cited answer.
message = next_hosted_turn(1, "How do I refund?", hits)
assert message.kind == "message"
assert message.citations == ("hosted-refund",)

# Example 3 — there is no step 2.
try:
    next_hosted_turn(2, "How do I refund?", hits)
    raise AssertionError("loop must cap")
except ValueError:
    pass

# Example 4 — empty hits still produce a message.
empty = next_hosted_turn(1, "??", [])
assert empty.text == "No hosted hits."

# Example 5 — this fake cannot teach live file_search latency or chunking.
print(message.text)
print("A.5 examples ok")
