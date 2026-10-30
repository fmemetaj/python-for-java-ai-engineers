"""USD from usage and data/pricing.yaml."""

from __future__ import annotations

from typing import Any


def cost_of(usage: dict[str, Any], model: str) -> float:
    """Compute USD. usage keys: input_tokens, output_tokens, cached_tokens (optional)."""
    raise NotImplementedError
