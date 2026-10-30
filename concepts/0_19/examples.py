"""Dataclass is a record; Pydantic validates at the boundary."""

from __future__ import annotations

from dataclasses import dataclass

from pydantic import BaseModel, Field, ValidationError


@dataclass(frozen=True)
class LogLine:
    level: str
    message: str


class TicketIn(BaseModel):
    id: int = Field(gt=0)
    subject: str = Field(min_length=2)


assert LogLine("INFO", "ok").level == "INFO"
TicketIn(id=1, subject="Login")
try:
    TicketIn(id=0, subject="x")
except ValidationError:
    pass
else:
    raise AssertionError("expected ValidationError")
print("0.19 examples ok")
