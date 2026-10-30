"""Configure the LLM client from env and build a Responses request body."""

from __future__ import annotations


def resolve_provider(provider: str | None, env: dict[str, str]) -> str:
    """Return fake/ollama/openai from an explicit name or LLM_PROVIDER, default fake."""
    raise NotImplementedError


def responses_body(model: str, instructions: str, user_input: str) -> dict[str, object]:
    """Return kwargs for POST /v1/responses (store false, input not messages)."""
    raise NotImplementedError


def key_leaked(log_line: str, key: str) -> bool:
    """True when a non-empty secret appears in the log line."""
    raise NotImplementedError
