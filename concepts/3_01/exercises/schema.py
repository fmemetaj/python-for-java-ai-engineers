"""Build Responses vs Chat Completions structured-output payloads and parse an Incident."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class Incident(BaseModel):
    service: str = Field(min_length=1)
    severity: Literal["low", "medium", "high", "critical"]
    summary: str = Field(min_length=1)
    timestamp: str = Field(min_length=1)


def incident_schema() -> dict[str, Any]:
    """JSON Schema for Incident with additionalProperties false."""
    raise NotImplementedError


def responses_format(schema: dict[str, Any]) -> dict[str, Any]:
    """Return the inner text.format object (type=json_schema, name=incident, strict)."""
    raise NotImplementedError


def chat_format(schema: dict[str, Any]) -> dict[str, Any]:
    """Return Chat Completions response_format (nested json_schema key)."""
    raise NotImplementedError


def parse_incident(text: str) -> Incident:
    """Validate a JSON string as Incident. Invalid payloads must raise ValidationError."""
    raise NotImplementedError
