"""Request ids, JSON logs, span duration."""

from __future__ import annotations


def pick_request_id(sdk_id: str, fallback: str) -> str:
    """Return sdk_id if it is non-empty after strip, else fallback, else req_local."""
    raise NotImplementedError


def json_log_line(event: str, request_id: str, cost_usd: float) -> str:
    """JSON object with event, request_id, cost_usd. Sorted keys."""
    raise NotImplementedError


def span_ms(start_ms: float, end_ms: float) -> float:
    """Non-negative duration in milliseconds."""
    raise NotImplementedError
