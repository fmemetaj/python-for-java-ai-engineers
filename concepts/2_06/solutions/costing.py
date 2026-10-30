"""USD from usage and data/pricing.yaml (solution)."""

from __future__ import annotations

from typing import Any

from course_kit.cost import cost_usd
from course_kit.llm import Usage


def cost_of(usage: dict[str, Any], model: str) -> float:
    """Compute USD. usage keys: input_tokens, output_tokens, cached_tokens (optional)."""
    parsed = Usage(
        input_tokens=int(usage["input_tokens"]),
        output_tokens=int(usage["output_tokens"]),
        total_tokens=int(
            usage.get("total_tokens", int(usage["input_tokens"]) + int(usage["output_tokens"]))
        ),
        cached_tokens=int(usage.get("cached_tokens", 0)),
    )
    return cost_usd(parsed, model)
