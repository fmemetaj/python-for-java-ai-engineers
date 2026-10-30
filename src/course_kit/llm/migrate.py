"""Helpers for Chat Completions → Responses. Official checklist:

https://platform.openai.com/docs/guides/migrate-to-responses
"""

from __future__ import annotations

from .base import ChatCompletion, LLMResponse


MIGRATION_ERRORS = (
    "choices[0].message.content instead of output_text",
    "treating every output entry as a message",
    "dropping reasoning items when replaying context",
    "response_format instead of text.format",
    "Chat Completions streaming chunks instead of typed SSE events",
    "assuming previous_response_id is free context",
)


def migrate_chat_body_to_responses(chat_body: dict[str, object]) -> dict[str, object]:
    """Convert a Chat Completions request dict to a Responses request dict.

    Maps `messages` → `input` + top-level `instructions` (system role).
    Maps `response_format` → `text.format`. Drops Assistants-only fields.
    """
    if "assistant_id" in chat_body:
        raise ValueError("Assistants API was sunset 2026-08-26; use Responses")
    model = chat_body.get("model")
    if not isinstance(model, str) or not model:
        raise ValueError("model is required")
    messages = chat_body.get("messages")
    if not isinstance(messages, list):
        raise ValueError("Chat Completions body needs messages[]")
    instructions = ""
    inputs: list[dict[str, str]] = []
    for item in messages:
        if not isinstance(item, dict):
            raise TypeError("each message must be a dict")
        role = str(item.get("role", ""))
        content = str(item.get("content", ""))
        if role == "system":
            instructions = content
        else:
            inputs.append({"role": role, "content": content})
    body: dict[str, object] = {
        "model": model,
        "input": inputs
        if len(inputs) != 1 or inputs[0]["role"] != "user"
        else inputs[0]["content"],
        "store": False,
    }
    if instructions:
        body["instructions"] = instructions
    if "response_format" in chat_body:
        body["text"] = {"format": chat_body["response_format"]}
    if "temperature" in chat_body:
        body["temperature"] = chat_body["temperature"]
    return body


def output_text_from_chat(completion: ChatCompletion) -> str:
    if not completion.choices:
        return ""
    return completion.choices[0].message.content


def output_text_from_responses(response: LLMResponse) -> str:
    return response.output_text
