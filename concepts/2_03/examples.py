"""Context-window arithmetic with a tiny toy window."""

from __future__ import annotations

from course_kit.llm.context import remaining_budget, would_overflow
from course_kit.llm.tokens import estimate_tokens

assert remaining_budget(100, 40, 20) == 40
assert would_overflow(100, ["x" * 360], 20) is True  # 360 chars → 90 tokens
assert would_overflow(100, ["abcd"], 1) is False
assert estimate_tokens("DocsDesk") >= 1
# Real gpt-4.1-mini window is 1047576 (data/pricing.yaml); we use 100 here.
print("2.3 examples ok")
