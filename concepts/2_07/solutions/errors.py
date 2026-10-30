"""Spot official migration errors and read either output shape (solution)."""

from __future__ import annotations

from typing import Any

MARKERS = (
    "choices[0].message.content",
    "response_format",
    "assistant_id",
    "chat.completion.chunk",
)


def is_migration_error(snippet: str) -> bool:
    """True if the snippet matches a common Chat Completions → Responses mistake."""
    lowered = snippet.lower()
    if "previous_response_id" in lowered and "free" in lowered:
        return True
    return any(marker.lower() in lowered for marker in MARKERS)


def extract_text(payload: dict[str, Any]) -> str:
    """Read assistant text from a Responses object or a Chat Completions object."""
    if payload.get("object") == "response" or "output" in payload:
        if "output_text" in payload and isinstance(payload["output_text"], str):
            return payload["output_text"]
        parts: list[str] = []
        for item in payload.get("output", []):
            if item.get("type") != "message":
                continue
            for block in item.get("content", []):
                if block.get("type") == "output_text":
                    parts.append(str(block.get("text", "")))
        return "".join(parts)
    choices = payload.get("choices") or []
    if choices:
        message = choices[0].get("message") or {}
        return str(message.get("content") or "")
    return ""
