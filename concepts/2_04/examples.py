"""Sampling is live-only; FakeLLM stays deterministic for CI."""

from __future__ import annotations

from course_kit.llm import FakeLLM, responses_create_kwargs

fake = FakeLLM(script={"hi": "hello"})
assert fake.complete("hi").output_text == fake.complete("hi").output_text
body = responses_create_kwargs(
    model="gpt-4.1-mini",
    instructions="",
    input="hi",
    temperature=0.2,
)
assert body["temperature"] == 0.2
print("2.4 examples ok")
