"""Optional local Ollama inference. No API key, no external action, no real sending."""

from __future__ import annotations

import json
from typing import Literal
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from pydantic import BaseModel, Field, ValidationError

from .models import Ticket


class OllamaUnavailable(RuntimeError):
    """The local Ollama service or model could not produce a valid reply."""


class ModelSuggestion(BaseModel):
    category: Literal["access", "billing", "general"]
    suggested_reply: str = Field(min_length=8, max_length=1200)


def analyze_with_ollama(ticket: Ticket, model: str = "llama3.2:1b") -> ModelSuggestion:
    """Request a validated draft from local Ollama; does NOT execute any external action.

    Endpoint is pinned to loopback. Treat generated content as untrusted draft text.
    """
    body = {
        "model": model,
        "stream": False,
        "format": "json",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You help triage fictional support tickets. Return ONLY a JSON object "
                    'with "category" (access, billing, or general) and "suggested_reply" '
                    "(a polite, short proposed answer). Do not claim to have taken an action."
                ),
            },
            {"role": "user", "content": ticket.model_dump_json()},
        ],
    }
    request = Request(
        "http://127.0.0.1:11434/api/chat",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=90) as response:
            data = json.load(response)
        return ModelSuggestion.model_validate_json(data["message"]["content"])
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        raise OllamaUnavailable(
            f"Cannot reach local Ollama or model '{model}'. "
            "Start Ollama and run: ollama pull llama3.2:1b"
        ) from exc
    except (KeyError, TypeError, ValueError, ValidationError) as exc:
        raise OllamaUnavailable(
            "The local model returned invalid JSON or unsupported fields. "
            "Retry, or switch the demo to Mock mode."
        ) from exc
