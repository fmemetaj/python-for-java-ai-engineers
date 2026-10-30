"""Typed Responses SSE events from FakeLLM."""

from __future__ import annotations

from course_kit.llm import FakeLLM

events = list(FakeLLM(script={"q": "WXYZ"}).stream("q"))
assert any(event.type == "response.output_text.delta" for event in events)
assert events[-1].type == "response.completed"
assert "".join(event.delta for event in events) == "WXYZ"
print("2.9 examples ok")
