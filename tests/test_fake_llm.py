"""Fake LLM is Responses-shaped, offline, and never uses the Assistants API."""

from __future__ import annotations

import os

import pytest

from course_kit.llm import FakeLLM, get_client, responses_create_kwargs


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


def test_openai_provider_is_opt_in() -> None:
    with pytest.raises(RuntimeError, match="responses.create"):
        get_client("openai")


def test_unknown_provider_rejected() -> None:
    with pytest.raises(ValueError, match="Unknown LLM_PROVIDER"):
        get_client("assistants")
