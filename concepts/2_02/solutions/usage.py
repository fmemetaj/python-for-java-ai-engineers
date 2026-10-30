"""Read a Responses-shaped usage payload (solution)."""

from __future__ import annotations

from typing import Any


def parse_usage(payload: dict[str, Any]) -> dict[str, int]:
    """Return input_tokens, output_tokens, total_tokens, cached_tokens."""
    details = payload.get("input_tokens_details") or {}
    cached = int(payload.get("cached_tokens", details.get("cached_tokens", 0)))
    input_tokens = int(payload["input_tokens"])
    output_tokens = int(payload["output_tokens"])
    total = int(payload.get("total_tokens", input_tokens + output_tokens))
    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total,
        "cached_tokens": cached,
    }


def uncached_input(payload: dict[str, Any]) -> int:
    """input_tokens minus cached_tokens."""
    parsed = parse_usage(payload)
    return parsed["input_tokens"] - parsed["cached_tokens"]
