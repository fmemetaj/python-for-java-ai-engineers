"""Settings from env; `.env` is local; Responses API if you opt into OpenAI."""

from __future__ import annotations

from course_kit.llm import responses_create_kwargs

body = responses_create_kwargs(
    model="gpt-4.1-mini",
    instructions="You are DocsDesk.",
    input="List auth steps",
)
assert body["input"] == "List auth steps"
assert "assistant_id" not in body
print("1.7 examples ok")
