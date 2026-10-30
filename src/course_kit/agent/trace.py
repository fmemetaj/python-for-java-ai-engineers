"""Agent-run tracing. Java analog: Micrometer / OpenTelemetry spans.

One AgentTrace per investigate() call. Nested spans are children, not a
separate distributed trace. This is in-process and offline — it does not
export to a collector.
https://opentelemetry.io/docs/concepts/signals/traces/
"""

from __future__ import annotations

import time
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any


def _now_ms() -> float:
    return time.monotonic() * 1000.0


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

    def end(self, extra: Mapping[str, Any] | None = None) -> None:
        if extra:
            self.attributes.update(dict(extra))
        self.end_ms = _now_ms()

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "kind": self.kind,
            "duration_ms": self.duration_ms,
            "attributes": dict(self.attributes),
            "children": [child.as_dict() for child in self.children],
        }


class AgentTrace:
    """A tree of spans for one agent run. request_id is the correlation key."""

    def __init__(self, request_id: str = "req_fake") -> None:
        self.request_id = request_id
        self.spans: list[Span] = []
        self._stack: list[Span] = []

    def start_span(
        self,
        name: str,
        kind: str,
        **attributes: Any,
    ) -> Span:
        span = Span(name=name, kind=kind, start_ms=_now_ms(), attributes=dict(attributes))
        if self._stack:
            self._stack[-1].children.append(span)
        else:
            self.spans.append(span)
        self._stack.append(span)
        return span

    def end_span(self, span: Span, extra: Mapping[str, Any] | None = None) -> None:
        span.end(extra)
        if self._stack and self._stack[-1] is span:
            self._stack.pop()
            return
        if span in self._stack:
            while self._stack and self._stack[-1] is not span:
                dangling = self._stack.pop()
                if dangling.end_ms is None:
                    dangling.end()
            if self._stack and self._stack[-1] is span:
                self._stack.pop()

    @contextmanager
    def span(self, name: str, kind: str, **attributes: Any) -> Iterator[Span]:
        current = self.start_span(name, kind, **attributes)
        try:
            yield current
        finally:
            self.end_span(current)

    def as_list(self) -> list[dict[str, Any]]:
        return [span.as_dict() for span in self.spans]
