"""Assemble Responses stream events."""

from __future__ import annotations

from typing import Any


def assemble_text(events: list[dict[str, Any]]) -> str:
    """Concatenate delta fields of response.output_text.delta events."""
    raise NotImplementedError


def is_responses_event(event_type: str) -> bool:
    """True for typed Responses SSE names (prefix response.)."""
    raise NotImplementedError
