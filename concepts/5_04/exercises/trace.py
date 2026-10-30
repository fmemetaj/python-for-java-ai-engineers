"""A tiny in-process span tree. Inject a clock for deterministic tests."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Span:
    name: str
    kind: str
    start_ms: float
    end_ms: float | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    children: list[Span] = field(default_factory=list)

    @property
    def duration_ms(self) -> float:
        raise NotImplementedError


class Trace:
    def __init__(self, clock: Callable[[], float], request_id: str = "req") -> None:
        self.clock = clock
        self.request_id = request_id
        self.spans: list[Span] = []
        self._stack: list[Span] = []

    def start_span(self, name: str, kind: str, **attributes: Any) -> Span:
        raise NotImplementedError

    def end_span(self, span: Span) -> None:
        raise NotImplementedError

    def as_list(self) -> list[dict[str, Any]]:
        raise NotImplementedError
