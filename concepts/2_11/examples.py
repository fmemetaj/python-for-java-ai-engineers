"""Reasoning tokens sit inside output_tokens."""

from __future__ import annotations

from course_kit.llm import FakeLLM

fake = FakeLLM(script={"q": "ok"})
none = fake.complete("q", reasoning_effort="none")
high = fake.complete("q", reasoning_effort="high")
assert none.usage.reasoning_tokens == 0
assert high.usage.reasoning_tokens == 256
assert high.output[0].type == "reasoning"
print("2.11 examples ok")
