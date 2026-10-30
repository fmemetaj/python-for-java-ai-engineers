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
        if self.end_ms is None:
            return 0.0
        return max(0.0, self.end_ms - self.start_ms)


class Trace:
    def __init__(self, clock: Callable[[], float], request_id: str = "req") -> None:
        self.clock = clock
        self.request_id = request_id
        self.spans: list[Span] = []
        self._stack: list[Span] = []

    def start_span(self, name: str, kind: str, **attributes: Any) -> Span:
        span = Span(
            name=name,
            kind=kind,
            start_ms=self.clock(),
            attributes=dict(attributes),
        )
        if self._stack:
            self._stack[-1].children.append(span)
        else:
            self.spans.append(span)
        self._stack.append(span)
        return span

    def end_span(self, span: Span) -> None:
        span.end_ms = self.clock()
        if self._stack and self._stack[-1] is span:
            self._stack.pop()

    def as_list(self) -> list[dict[str, Any]]:
        return [_as_dict(span) for span in self.spans]


def _as_dict(span: Span) -> dict[str, Any]:
    return {
        "name": span.name,
        "kind": span.kind,
        "duration_ms": span.duration_ms,
        "attributes": dict(span.attributes),
        "children": [_as_dict(child) for child in span.children],
    }
