"""Guided: route a question to ask vs investigate."""

from __future__ import annotations

_HINTS = ("500", "incident", "investigate", "triage")


def route_intent(text: str) -> str:
    """Return investigate if the text looks like an incident, else ask."""
    lowered = text.lower()
    if any(token in lowered for token in _HINTS):
        return "investigate"
    return "ask"
