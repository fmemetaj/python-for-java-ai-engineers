"""Same DocsDesk question in both API shapes."""

from __future__ import annotations

from course_kit.llm import FakeLLM, chat_completions_create_kwargs, responses_create_kwargs
from course_kit.llm.migrate import migrate_chat_body_to_responses, output_text_from_chat

fake = FakeLLM(script={"What is auth?": "Bearer token"})
chat_body = chat_completions_create_kwargs(
    model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": "You are DocsDesk."},
        {"role": "user", "content": "What is auth?"},
    ],
)
resp_body = migrate_chat_body_to_responses(chat_body)
assert resp_body["instructions"] == "You are DocsDesk."
assert resp_body["input"] == "What is auth?"
assert "assistant_id" not in responses_create_kwargs(
    model="gpt-4.1-mini", instructions="You are DocsDesk.", input="What is auth?"
)
chat = fake.chat([{"role": "user", "content": "What is auth?"}])
assert output_text_from_chat(chat) == "Bearer token"
assert fake.complete("What is auth?").object == "response"
print("2.7 examples ok")
