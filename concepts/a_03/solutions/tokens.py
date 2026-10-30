"""Image token counts and USD. Prices are arguments — do not hard-code rates."""

from __future__ import annotations

from course_kit.vision import image_cost_usd, image_token_count


def image_tokens(detail: str, width: int, height: int) -> int:
    """low → 85. high → 85 + 170 * 512px tiles after the published scale steps."""
    return image_token_count(detail, width, height)


def vision_cost_usd(
    *,
    image_tokens: int,
    text_input_tokens: int,
    output_tokens: int,
    input_per_million: float,
    output_per_million: float,
) -> float:
    """Images add to input tokens at the input rate."""
    return image_cost_usd(
        image_tokens=image_tokens,
        text_input_tokens=text_input_tokens,
        output_tokens=output_tokens,
        input_per_million=input_per_million,
        output_per_million=output_per_million,
    )
