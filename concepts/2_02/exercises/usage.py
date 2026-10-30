"""Read a Responses-shaped usage payload."""

from __future__ import annotations

from typing import Any


def parse_usage(payload: dict[str, Any]) -> dict[str, int]:
    """Return input_tokens, output_tokens, total_tokens, cached_tokens."""
    raise NotImplementedError


def uncached_input(payload: dict[str, Any]) -> int:
    """input_tokens minus cached_tokens."""
    raise NotImplementedError
