"""Stored state still bills prior input; trimming drops oldest turns."""

from __future__ import annotations

from course_kit.llm import FakeLLM
from course_kit.llm.context import trim_oldest

fake = FakeLLM()
first = fake.complete("How do clients authenticate?", store=True)
second = fake.complete("follow-up", previous_response_id=first.id, store=True)
assert second.usage.input_tokens > first.usage.input_tokens
kept = trim_oldest(["aaaa", "bbbb", "cccc"], budget=2)
assert kept[-1] == "cccc"
print("2.8 examples ok")
