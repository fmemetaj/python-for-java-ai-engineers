"""Configure an LLM client from env — no network, no key required."""

from __future__ import annotations

import os

from course_kit.llm import FakeLLM, get_client, responses_create_kwargs

previous = os.environ.pop("LLM_PROVIDER", None)
try:
    client = get_client()
finally:
    if previous is not None:
        os.environ["LLM_PROVIDER"] = previous
assert isinstance(client, FakeLLM)

body = responses_create_kwargs(
    model="gpt-4.1-mini",
    instructions="You are DocsDesk.",
    input="What is auth?",
)
assert body["input"] == "What is auth?"
assert "messages" not in body
assert "assistant_id" not in body
assert body["store"] is False

reply = FakeLLM(script={"What is auth?": "Bearer token"}).complete("What is auth?")
assert reply.object == "response"
assert "Bearer" in reply.output_text
print("2.1 examples ok")
