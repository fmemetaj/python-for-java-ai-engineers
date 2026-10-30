"""Hand-computed cost fixtures against data/pricing.yaml (2026-10-30)."""

from __future__ import annotations

import pytest
from course_kit.cost import cost_usd, format_cost, load_pricing
from course_kit.llm import Usage


def test_pricing_table_is_dated_and_sourced() -> None:
    table = load_pricing()
    assert table.source == "https://platform.openai.com/docs/pricing"
    assert table.retrieved == "2026-10-30"
    assert table.unit_tokens == 1_000_000
    assert "gpt-4.1-mini" in table.models
    assert "gpt-5-mini" in table.models


def test_gpt41_mini_uncached() -> None:
    # 1000 in * $0.40/1M + 500 out * $1.60/1M = 0.0004 + 0.0008 = 0.0012
    usage = Usage(input_tokens=1000, output_tokens=500, total_tokens=1500)
    assert cost_usd(usage, "gpt-4.1-mini") == pytest.approx(0.0012)


def test_gpt41_mini_with_cached_input() -> None:
    # 200 uncached * 0.40/1M + 800 cached * 0.10/1M + 500 out * 1.60/1M
    # = 0.00008 + 0.00008 + 0.0008 = 0.00096
    usage = Usage(
        input_tokens=1000,
        output_tokens=500,
        total_tokens=1500,
        cached_tokens=800,
    )
    assert cost_usd(usage, "gpt-4.1-mini") == pytest.approx(0.00096)


def test_gpt5_mini_cached_rate() -> None:
    # 1_000_000 in, all cached, 0 out → $0.025
    usage = Usage(
        input_tokens=1_000_000,
        output_tokens=0,
        total_tokens=1_000_000,
        cached_tokens=1_000_000,
    )
    assert cost_usd(usage, "gpt-5-mini") == pytest.approx(0.025)


def test_unknown_model_rejected() -> None:
    usage = Usage(input_tokens=1, output_tokens=1, total_tokens=2)
    with pytest.raises(KeyError, match="Unknown model"):
        cost_usd(usage, "gpt-assistants-sunset")


def test_cached_cannot_exceed_input() -> None:
    usage = Usage(input_tokens=10, output_tokens=0, total_tokens=10, cached_tokens=11)
    with pytest.raises(ValueError, match="cached_tokens"):
        cost_usd(usage, "gpt-4.1-mini")


def test_format_cost() -> None:
    assert format_cost(0.0012).startswith("$0.0012")
