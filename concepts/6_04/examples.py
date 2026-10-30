"""Cost control: budgets, routing, prompt cache, dashboard. Offline FakeLLM."""

from __future__ import annotations

from course_kit.cost import load_pricing
from course_kit.llm.base import Usage
from docsdesk.budget import (
    CHEAP_MODEL,
    DEFAULT_MODEL,
    BudgetExceededError,
    cache_discount_usd,
    cost_of,
    costs_from_logs,
    remaining,
    route_model,
    within_budget,
)

# Example 1 — remaining USD.
assert remaining(1.0, 0.4) == 0.6
assert within_budget(0.4, 1.0) is True

# Example 2 — spent past the cap is not within budget.
assert within_budget(1.2, 1.0) is False

# Example 3 — route to nano when the remainder cannot cover the estimate.
assert route_model(1.0, estimated_usd=0.0001) == DEFAULT_MODEL
assert route_model(0.00005, estimated_usd=0.01) == CHEAP_MODEL
try:
    route_model(0.0, estimated_usd=0.01)
    raise AssertionError("zero remainder must refuse")
except BudgetExceededError:
    pass

# Example 4 — cached tokens are cheaper, not free. Mini rates from pricing.yaml.
prices = load_pricing().models["gpt-4.1-mini"]
saved = cache_discount_usd(
    cached_tokens=1000,
    input_per_million=prices.input_per_million,
    cached_input_per_million=prices.cached_input_per_million,
)
assert abs(saved - 0.0003) < 1e-12
cached_usage = Usage(input_tokens=2000, output_tokens=0, total_tokens=2000, cached_tokens=1000)
full_usage = Usage(input_tokens=2000, output_tokens=0, total_tokens=2000, cached_tokens=0)
assert cost_of(cached_usage, "gpt-4.1-mini") < cost_of(full_usage, "gpt-4.1-mini")

# Example 5 — dashboard = sum of JSON cost fields.
lines = [
    '{"cost_usd":0.000040,"event":"docsdesk.ask","request_id":"req_fake_0001"}',
    '{"cost_usd":0.000010,"event":"docsdesk.ask","request_id":"req_fake_0002"}',
]
assert abs(costs_from_logs(lines) - 0.00005) < 1e-12

print("6.4 examples ok")
