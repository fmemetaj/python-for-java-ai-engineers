"""Configure the LLM client from env and build a Responses request body (solution)."""

from __future__ import annotations


def resolve_provider(provider: str | None, env: dict[str, str]) -> str:
    """Return fake/ollama/openai from an explicit name or LLM_PROVIDER, default fake."""
    name = (provider or env.get("LLM_PROVIDER") or "fake").strip().lower()
    return name or "fake"


def responses_body(model: str, instructions: str, user_input: str) -> dict[str, object]:
    """Return kwargs for POST /v1/responses (store false, input not messages)."""
    return {
        "model": model,
        "instructions": instructions,
        "input": user_input,
        "store": False,
    }


def key_leaked(log_line: str, key: str) -> bool:
    """True when a non-empty secret appears in the log line."""
    return bool(key) and key in log_line
