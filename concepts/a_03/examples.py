"""Image tokens bill as input. Prices from data/pricing.yaml."""

from __future__ import annotations

from course_kit.cost import load_pricing
from course_kit.vision import image_cost_usd, image_token_count

# Example 1 — low detail is a flat 85 tokens regardless of pixel size.
assert image_token_count("low", 64, 64) == 85
assert image_token_count("low", 4000, 3000) == 85

# Example 2 — high detail uses 512px tiles after scaling.
assert image_token_count("high", 1024, 768) == 765

# Example 3 — images are input, not output.
table = load_pricing()
row = table.models["gpt-4.1-mini"]
amount = image_cost_usd(
    image_tokens=85,
    text_input_tokens=0,
    output_tokens=0,
    input_per_million=row.input_per_million,
    output_per_million=row.output_per_million,
)
expected = 85 * row.input_per_million / 1_000_000
assert abs(amount - expected) < 1e-12

# Example 4 — never hard-code the rate in lesson prose; read the dated YAML.
assert table.source.startswith("https://platform.openai.com")

# Example 5 — a 4K screenshot on high detail costs more tiles, not more megabytes.
big = image_token_count("high", 4000, 3000)
assert big > 85
print(f"high-4k tokens={big}")
print("A.3 examples ok")
