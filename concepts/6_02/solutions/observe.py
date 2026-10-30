"""Request ids, JSON logs, span duration."""

from __future__ import annotations

import json


def pick_request_id(sdk_id: str, fallback: str) -> str:
    """Return sdk_id if it is non-empty after strip, else fallback, else req_local."""
    text = sdk_id.strip()
    if text:
        return text
    return fallback.strip() or "req_local"


def json_log_line(event: str, request_id: str, cost_usd: float) -> str:
    """JSON object with event, request_id, cost_usd. Sorted keys."""
    payload = {"cost_usd": cost_usd, "event": event, "request_id": request_id}
    return json.dumps(payload, separators=(",", ":"), sort_keys=True)


def span_ms(start_ms: float, end_ms: float) -> float:
    """Non-negative duration in milliseconds."""
    return max(0.0, end_ms - start_ms)
