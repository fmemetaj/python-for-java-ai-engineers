"""Fake LLM is Responses-shaped, Chat-Completions-shaped, offline, no Assistants API."""

from __future__ import annotations

import os

import pytest

from course_kit.llm import (
    FakeLLM,
    chat_completions_create_kwargs,
    get_client,
    json_schema_from_model,
    responses_create_kwargs,
    responses_text_format,
)
from course_kit.llm.migrate import migrate_chat_body_to_responses, output_text_from_chat


def test_fake_is_default_client() -> None:
    previous = os.environ.get("LLM_PROVIDER")
    os.environ.pop("LLM_PROVIDER", None)
    try:
        client = get_client()
        result = client.complete("Summarize tickets")
    finally:
        if previous is None:
            os.environ.pop("LLM_PROVIDER", None)
        else:
            os.environ["LLM_PROVIDER"] = previous
    assert result.object == "response"
    assert result.output[0].type == "message"
    assert result.output_text
    assert result.usage.total_tokens >= result.usage.input_tokens


def test_scripted_reply() -> None:
    client = FakeLLM(script={"ping": "pong"})
    assert client.complete("ping").output_text == "pong"


def test_request_id_is_not_response_id() -> None:
    client = FakeLLM(script={"ping": "pong"})
    response = client.complete("ping")
    assert response.request_id.startswith("req_fake_")
    assert response.id.startswith("resp_fake_")
    assert response.request_id != response.id


def test_responses_kwargs_are_current_api() -> None:
    body = responses_create_kwargs(
        model="gpt-4.1-mini",
        instructions="You are DocsDesk.",
        input="What is auth?",
    )
    assert body["input"] == "What is auth?"
    assert "messages" not in body
    assert "assistant_id" not in body
    assert body["store"] is False


def test_chat_completions_kwargs_use_messages() -> None:
    body = chat_completions_create_kwargs(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": "Hi"}],
    )
    messages = body["messages"]
    assert isinstance(messages, list)
    first = messages[0]
    assert isinstance(first, dict)
    assert first["content"] == "Hi"
    assert "input" not in body
    assert "assistant_id" not in body


def test_chat_shape() -> None:
    client = FakeLLM(script={"hello": "world"})
    completion = client.chat([{"role": "user", "content": "hello"}])
    assert completion.object == "chat.completion"
    assert output_text_from_chat(completion) == "world"
    assert completion.usage.prompt_tokens >= 1


def test_previous_response_id_still_bills_prior_input() -> None:
    client = FakeLLM()
    first = client.complete("How do clients authenticate?", store=True)
    second = client.complete(
        "follow-up",
        previous_response_id=first.id,
        store=True,
    )
    assert second.usage.input_tokens > first.usage.input_tokens
    assert second.previous_response_id == first.id


def test_streaming_typed_events() -> None:
    client = FakeLLM(script={"stream me": "ABCD"})
    events = list(client.stream("stream me"))
    types = [event.type for event in events]
    assert "response.output_text.delta" in types
    assert types[-1] == "response.completed"
    assembled = "".join(event.delta for event in events)
    assert assembled == "ABCD"


def test_reasoning_tokens_are_inside_output_tokens() -> None:
    client = FakeLLM(script={"q": "ok"})
    none = client.complete("q", reasoning_effort="none")
    high = client.complete("q", reasoning_effort="high")
    assert none.usage.reasoning_tokens == 0
    assert high.usage.reasoning_tokens > 0
    assert high.usage.output_tokens == high.usage.reasoning_tokens + none.usage.output_tokens
    assert any(item.type == "reasoning" for item in high.output)


def test_migrate_chat_to_responses() -> None:
    chat = {
        "model": "gpt-4.1-mini",
        "messages": [
            {"role": "system", "content": "You are DocsDesk."},
            {"role": "user", "content": "What is auth?"},
        ],
        "response_format": {"type": "text"},
    }
    body = migrate_chat_body_to_responses(chat)
    assert body["input"] == "What is auth?"
    assert body["instructions"] == "You are DocsDesk."
    assert body["store"] is False
    assert "messages" not in body
    assert body["text"] == {"format": {"type": "text"}}


def test_migrate_rejects_assistants() -> None:
    with pytest.raises(ValueError, match="sunset"):
        migrate_chat_body_to_responses({"model": "gpt-4.1-mini", "assistant_id": "asst_x"})


def test_openai_provider_is_opt_in() -> None:
    with pytest.raises(RuntimeError, match="responses.create"):
        get_client("openai")


def test_unknown_provider_rejected() -> None:
    with pytest.raises(ValueError, match="Unknown LLM_PROVIDER"):
        get_client("assistants")


def test_structured_output_and_refusal() -> None:
    from docsdesk.models import Incident

    payload = {
        "service": "auth",
        "severity": "high",
        "summary": "token validation failed",
        "timestamp": "2026-10-30T08:00:00Z",
    }
    schema = json_schema_from_model(Incident)
    fmt = responses_text_format("incident", schema)
    client = FakeLLM(structured={"extract": payload}, refusals=("nope",))
    response = client.complete("extract", text_format=fmt)
    assert response.output_parsed == payload
    refused = client.complete("nope")
    assert refused.refusal
    assert refused.function_calls == ()


def test_scripted_function_call_then_output() -> None:
    client = FakeLLM(
        tool_calls={
            "q": [
                {
                    "call_id": "call_1",
                    "name": "search_docs",
                    "arguments": '{"query":"auth"}',
                }
            ]
        },
        after_tools={"q": "found it"},
    )
    tools: list[dict[str, object]] = [{"type": "function", "name": "search_docs"}]
    first = client.complete("q", tools=tools)
    assert first.function_calls[0].call_id == "call_1"
    second = client.complete(
        "q",
        tools=tools,
        input_items=[
            {
                "type": "function_call_output",
                "call_id": "call_1",
                "output": "[]",
            }
        ],
    )
    assert second.output_text == "found it"
    assert second.function_calls == ()


def test_trajectory_advances_per_complete() -> None:
    client = FakeLLM(
        trajectories={
            "job": [
                {
                    "tools": [
                        {
                            "call_id": "c1",
                            "name": "search_docs",
                            "arguments": "{}",
                        }
                    ]
                },
                {"message": '{"ok":true}'},
            ]
        }
    )
    first = client.complete("job", tools=[{"type": "function", "name": "search_docs"}])
    assert first.function_calls[0].call_id == "c1"
    second = client.complete(
        "job",
        input_items=[
            {"type": "function_call_output", "call_id": "c1", "output": "[]"},
        ],
    )
    assert second.output_text == '{"ok":true}'
    assert second.function_calls == ()
    third = client.complete("job")
    assert third.output_text == '{"ok":true}'
