"""Structured logs, spans, and request IDs for DocsDesk production.

Java analog: Micrometer / OpenTelemetry + MDC. Module 5's AgentTrace is the
agent-loop tree; this module is the *request* correlation layer you ship:
every log line carries ``request_id``, and cost is a field, not a print().

The OpenAI Python SDK exposes the HTTP id as ``response._request_id``
(https://github.com/openai/openai-python). DocsDesk copies it onto
``LLMResponse.request_id`` (no leading underscore). That is *not* ``response.id``.

This tracer is in-process and offline. It does not export to a collector.
https://opentelemetry.io/docs/concepts/signals/traces/
https://docs.python.org/3/library/contextvars.html
"""

from __future__ import annotations

import json
import time
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any

from course_kit.llm.base import LLMResponse

_request_id: ContextVar[str] = ContextVar("docsdesk_request_id", default="")


def pick_request_id(sdk_id: str, fallback: str) -> str:
    """Prefer the provider HTTP request id; otherwise a local fallback."""
    text = sdk_id.strip()
    if text:
        return text
    return fallback.strip() or "req_local"


def bind_request_id(value: str) -> str:
    """Put ``value`` in the contextvar (MDC analog) and return it."""
    token = value.strip() or "req_local"
    _request_id.set(token)
    return token


def bind_from_response(response: LLMResponse, *, fallback: str = "") -> str:
    """Copy ``response.request_id`` into the contextvar."""
    return bind_request_id(pick_request_id(response.request_id, fallback))


def current_request_id() -> str:
    return _request_id.get()


def structured_event(event: str, **fields: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {"event": event, "request_id": current_request_id()}
    payload.update(fields)
    return payload


def format_json_log(event: str, **fields: Any) -> str:
    """One JSON object per line. Secrets must already be redacted by the caller."""
    return json.dumps(structured_event(event, **fields), separators=(",", ":"), sort_keys=True)


def span_ms(start_ms: float, end_ms: float) -> float:
    return max(0.0, end_ms - start_ms)


@dataclass
class RequestSpan:
    name: str
    start_ms: float
    end_ms: float | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    request_id: str = ""

    @property
    def duration_ms(self) -> float:
        end = self.end_ms if self.end_ms is not None else time.monotonic() * 1000.0
        return span_ms(self.start_ms, end)

    def finish(self, extra: dict[str, Any] | None = None) -> None:
        if extra:
            self.attributes.update(extra)
        if self.end_ms is None:
            self.end_ms = time.monotonic() * 1000.0

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "duration_ms": self.duration_ms,
            "request_id": self.request_id,
            "attributes": dict(self.attributes),
        }


@contextmanager
def start_span(name: str, **attributes: Any) -> Iterator[RequestSpan]:
    span = RequestSpan(
        name=name,
        start_ms=time.monotonic() * 1000.0,
        attributes=dict(attributes),
        request_id=current_request_id(),
    )
    try:
        yield span
    finally:
        span.finish()


__all__ = [
    "RequestSpan",
    "bind_from_response",
    "bind_request_id",
    "current_request_id",
    "format_json_log",
    "pick_request_id",
    "span_ms",
    "start_span",
    "structured_event",
]
