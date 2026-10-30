"""Image token counts and USD. Prices are arguments — do not hard-code rates."""

from __future__ import annotations


def image_tokens(detail: str, width: int, height: int) -> int:
    """low → 85. high → 85 + 170 * 512px tiles after the published scale steps."""
    raise NotImplementedError


def vision_cost_usd(
    *,
    image_tokens: int,
    text_input_tokens: int,
    output_tokens: int,
    input_per_million: float,
    output_per_million: float,
) -> float:
    """Images add to input tokens at the input rate."""
    raise NotImplementedError
