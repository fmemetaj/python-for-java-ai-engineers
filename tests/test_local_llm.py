"""Offline unit tests: real Ollama is never required for CI."""

import json
from urllib.error import URLError

import pytest

from mini_agent import Ticket
from mini_agent.local_llm import (
    ModelSuggestion,
    OllamaUnavailable,
    analyze_with_ollama,
)


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return None

    def read(self, *_args):
        return json.dumps(self.payload).encode("utf-8")


def ticket():
    return Ticket(id=1, subject="Login help", body="Cannot log in")


def test_validated_local_llm_response(monkeypatch):
    def fake_open(request, timeout):
        assert request.full_url == "http://127.0.0.1:11434/api/chat"
        body = json.loads(request.data)
        assert body["stream"] is False
        assert body["format"] == "json"
        assert timeout == 90
        return FakeResponse(
            {
                "message": {
                    "content": '{"category":"access","suggested_reply":"Please reset your password."}'
                }
            }
        )

    monkeypatch.setattr("mini_agent.local_llm.urlopen", fake_open)
    result = analyze_with_ollama(ticket())
    assert isinstance(result, ModelSuggestion)
    assert result.category == "access"


def test_rejects_invalid_model_output(monkeypatch):
    monkeypatch.setattr(
        "mini_agent.local_llm.urlopen",
        lambda *_args, **_kwargs: FakeResponse(
            {"message": {"content": '{"category":"invalid","suggested_reply":"No"}'}}
        ),
    )
    with pytest.raises(OllamaUnavailable, match="invalid JSON"):
        analyze_with_ollama(ticket())


def test_ollama_not_running_is_actionable(monkeypatch):
    def unavailable(*_args, **_kwargs):
        raise URLError("connection refused")

    monkeypatch.setattr("mini_agent.local_llm.urlopen", unavailable)
    with pytest.raises(OllamaUnavailable, match="ollama pull"):
        analyze_with_ollama(ticket())
