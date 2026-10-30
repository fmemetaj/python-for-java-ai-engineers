"""Hand-computed fixture costs from data/pricing.yaml."""

from __future__ import annotations

from course_kit.cost import cost_usd
from course_kit.llm import Usage

u = Usage(input_tokens=1000, output_tokens=500, total_tokens=1500)
assert abs(cost_usd(u, "gpt-4.1-mini") - 0.0012) < 1e-12
cached = Usage(input_tokens=1000, output_tokens=500, total_tokens=1500, cached_tokens=800)
assert abs(cost_usd(cached, "gpt-4.1-mini") - 0.00096) < 1e-12
print("2.6 examples ok")
