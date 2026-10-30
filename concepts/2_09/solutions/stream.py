"""Assemble Responses stream events (solution)."""

from __future__ import annotations

from typing import Any


def assemble_text(events: list[dict[str, Any]]) -> str:
    """Concatenate delta fields of response.output_text.delta events."""
    parts: list[str] = []
    for event in events:
        if event.get("type") == "response.output_text.delta":
            parts.append(str(event.get("delta") or ""))
    return "".join(parts)


def is_responses_event(event_type: str) -> bool:
    """True for typed Responses SSE names (prefix response.)."""
    return event_type.startswith("response.")
