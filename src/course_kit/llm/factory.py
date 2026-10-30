"""Provider switch from env. Default `fake` so CI and learners stay offline."""

from __future__ import annotations

import os

from .base import LLMClient
from .fake import FakeLLM

VALID_PROVIDERS = ("fake", "ollama", "openai")


def responses_create_kwargs(
    *,
    model: str,
    instructions: str,
    input: str,
) -> dict[str, object]:
    """Body for the current OpenAI Responses API (`POST /v1/responses`).

    This is **not** Chat Completions (`messages`) and **not** the Assistants API
    (sunset 2026-08-26). Official guide:
    https://platform.openai.com/docs/guides/migrate-to-responses
    """
    return {
        "model": model,
        "instructions": instructions,
        "input": input,
        "store": False,
    }


def get_client(provider: str | None = None) -> LLMClient:
    """Return an LLMClient. Unknown or live providers stay explicit and optional.

    Java analogy: `llmProvider` is a Spring profile. Tests and CI use `fake`.
    """
    name = (provider or os.environ.get("LLM_PROVIDER") or "fake").strip().lower()
    if name == "fake" or name == "":
        return FakeLLM()
    if name == "openai":
        raise RuntimeError(
            "Live OpenAI is optional. Keep LLM_PROVIDER=fake for the course. "
            "If you opt in, call client.responses.create with "
            "responses_create_kwargs(...) — never the sunset Assistants API."
        )
    if name == "ollama":
        raise RuntimeError(
            "Ollama is an optional local path (loopback only). "
            "Keep LLM_PROVIDER=fake in CI and for graded exercises."
        )
    valid = ", ".join(VALID_PROVIDERS)
    raise ValueError(f"Unknown LLM_PROVIDER={name!r}. Use one of: {valid}.")
