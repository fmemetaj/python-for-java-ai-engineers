"""Dataclass for trusted data; Pydantic at the untrusted boundary."""

from __future__ import annotations

from dataclasses import dataclass

from pydantic import BaseModel, Field


@dataclass(frozen=True)
class LogLine:
    level: str
    message: str


class TicketIn(BaseModel):
    id: int = Field(gt=0)
    subject: str = Field(min_length=2)


def parse_log_line(raw: str) -> LogLine | None:
    """Split 'LEVEL message'. Return None for blanks."""
    raise NotImplementedError


def parse_ticket(data: dict[str, object]) -> TicketIn:
    """Validate with Pydantic (model_validate)."""
    raise NotImplementedError
