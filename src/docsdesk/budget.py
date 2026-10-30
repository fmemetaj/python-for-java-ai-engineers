"""Per-request budgets, model routing, prompt-cache cost, log dashboards.

Token economics (Module 2) told you *how much a call costs*. This module
decides *whether to make it* and *on which model*. Prompt caching is billed
at the cached input rate in ``data/pricing.yaml``
(https://platform.openai.com/docs/guides/prompt-caching).

There is no honest Java analog for metered token routing. Cloud invoice
alerts are a loose cousin; they fire after the spend.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from course_kit.cost import cost_usd
from course_kit.llm.base import Usage

CHEAP_MODEL = "gpt-4.1-nano"
DEFAULT_MODEL = "gpt-4.1-mini"


class BudgetExceededError(RuntimeError):
    """Raised when the next call would exceed the remaining budget."""


@dataclass
class Budget:
    """A remaining USD allowance. ``spent`` only grows; tests inject a clock-free ledger."""

    limit_usd: float
    spent_usd: float = 0.0
    model: str = DEFAULT_MODEL

    @property
    def remaining_usd(self) -> float:
        return max(0.0, self.limit_usd - self.spent_usd)

    def debit(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("debit must be >= 0")
        self.spent_usd += amount


def remaining(limit_usd: float, spent_usd: float) -> float:
    if spent_usd < 0 or limit_usd < 0:
        raise ValueError("limit and spent must be >= 0")
    return max(0.0, limit_usd - spent_usd)


def within_budget(spent_usd: float, limit_usd: float) -> bool:
    return remaining(limit_usd, spent_usd) >= 0 and spent_usd <= limit_usd


def route_model(remaining_usd: float, *, estimated_usd: float) -> str:
    """Pick nano when the remaining budget is tight; mini otherwise.

    Raises BudgetExceededError when remaining USD cannot cover the next call.
    """
    if estimated_usd < 0 or remaining_usd < 0:
        raise ValueError("usd amounts must be >= 0")
    if remaining_usd <= 0:
        raise BudgetExceededError("remaining budget cannot cover the next call")
    if remaining_usd < estimated_usd:
        return CHEAP_MODEL
    return DEFAULT_MODEL


def cost_of(usage: Usage, model: str) -> float:
    """USD including cached-input discount. Same formula as Module 2."""
    return cost_usd(usage, model)


def cache_discount_usd(
    *,
    cached_tokens: int,
    input_per_million: float,
    cached_input_per_million: float,
    unit_tokens: int = 1_000_000,
) -> float:
    """What you *saved* versus billing cached tokens at the full input rate."""
    if cached_tokens < 0:
        raise ValueError("cached_tokens must be >= 0")
    return cached_tokens * (input_per_million - cached_input_per_million) / float(unit_tokens)


def total_cost(rows: list[dict[str, Any]]) -> float:
    """Sum ``cost_usd`` from structured log objects (already parsed)."""
    return sum(float(row.get("cost_usd") or 0.0) for row in rows)


def costs_from_logs(lines: list[str]) -> float:
    """Parse JSON log lines and sum cost_usd. Skip unreadable lines."""
    rows: list[dict[str, Any]] = []
    for line in lines:
        try:
            loaded = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(loaded, dict):
            rows.append(loaded)
    return total_cost(rows)


@dataclass
class CostLedger:
    """In-memory dashboard used by ProductionDesk tests."""

    lines: list[str] = field(default_factory=list)

    def record(self, line: str) -> None:
        self.lines.append(line)

    def total(self) -> float:
        return costs_from_logs(self.lines)


__all__ = [
    "CHEAP_MODEL",
    "DEFAULT_MODEL",
    "Budget",
    "BudgetExceededError",
    "CostLedger",
    "cache_discount_usd",
    "cost_of",
    "costs_from_logs",
    "remaining",
    "route_model",
    "total_cost",
    "within_budget",
]
