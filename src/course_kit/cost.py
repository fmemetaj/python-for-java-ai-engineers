"""USD cost from Responses-shaped usage and `data/pricing.yaml`.

Never hard-code prices in lesson prose. The YAML file is dated and sourced
from https://platform.openai.com/docs/pricing (retrieved 2026-10-30).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .loader import repo_root
from .llm.base import Usage

PRICING_PATH = Path("data") / "pricing.yaml"


@dataclass(frozen=True)
class ModelPrice:
    model: str
    input_per_million: float
    output_per_million: float
    cached_input_per_million: float
    context_window: int
    max_output_tokens: int


@dataclass(frozen=True)
class PricingTable:
    source: str
    retrieved: str
    currency: str
    unit_tokens: int
    models: dict[str, ModelPrice]


def _parse_scalar(raw: str) -> str | int | float:
    text = raw.strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in {"'", '"'}:
        return text[1:-1]
    if text.isdigit() or (text.startswith("-") and text[1:].isdigit()):
        return int(text)
    try:
        return float(text)
    except ValueError:
        return text


def _load_course_yaml(path: Path) -> dict[str, Any]:
    """Load the two-level mapping used by `data/pricing.yaml`. Not a general parser."""
    root: dict[str, Any] = {}
    current_map: dict[str, Any] | None = None
    nested: dict[str, Any] | None = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()
        if ":" not in line:
            continue
        key, _, rest = line.partition(":")
        key = key.strip()
        rest = rest.strip()
        if indent == 0:
            nested = None
            current_map = None
            if rest == "":
                current_map = {}
                root[key] = current_map
            else:
                root[key] = _parse_scalar(rest)
        elif indent == 2 and current_map is not None:
            if rest == "":
                nested = {}
                current_map[key] = nested
            else:
                nested = None
                current_map[key] = _parse_scalar(rest)
        elif indent == 4 and nested is not None:
            nested[key] = _parse_scalar(rest)
    return root


def load_pricing(path: Path | None = None) -> PricingTable:
    yaml_path = path if path is not None else repo_root() / PRICING_PATH
    data = _load_course_yaml(yaml_path)
    models_raw = data["models"]
    if not isinstance(models_raw, dict):
        raise ValueError("pricing.yaml models must be a mapping")
    models: dict[str, ModelPrice] = {}
    for name, raw in models_raw.items():
        if not isinstance(raw, dict):
            raise ValueError(f"pricing for {name!r} must be a mapping")
        models[str(name)] = ModelPrice(
            model=str(name),
            input_per_million=float(raw["input_per_million"]),
            output_per_million=float(raw["output_per_million"]),
            cached_input_per_million=float(raw["cached_input_per_million"]),
            context_window=int(raw["context_window"]),
            max_output_tokens=int(raw["max_output_tokens"]),
        )
    return PricingTable(
        source=str(data["source"]),
        retrieved=str(data["retrieved"]),
        currency=str(data["currency"]),
        unit_tokens=int(data["unit_tokens"]),
        models=models,
    )


def cost_usd(usage: Usage, model: str, table: PricingTable | None = None) -> float:
    """Return USD for this call. Cached tokens are billed at the cached input rate.

    Uncached input = input_tokens - cached_tokens.
    Reasoning tokens are already inside `output_tokens` (billed as output).
    """
    prices = table if table is not None else load_pricing()
    try:
        row = prices.models[model]
    except KeyError as exc:
        known = ", ".join(sorted(prices.models))
        raise KeyError(f"Unknown model {model!r}. Known: {known}") from exc
    if usage.cached_tokens < 0 or usage.input_tokens < 0 or usage.output_tokens < 0:
        raise ValueError("token counts must be >= 0")
    if usage.cached_tokens > usage.input_tokens:
        raise ValueError("cached_tokens cannot exceed input_tokens")
    uncached = usage.input_tokens - usage.cached_tokens
    million = float(prices.unit_tokens)
    return (
        uncached * row.input_per_million / million
        + usage.cached_tokens * row.cached_input_per_million / million
        + usage.output_tokens * row.output_per_million / million
    )


def format_cost(amount: float) -> str:
    """Fixed 6 decimal places so tiny fixture bills stay readable."""
    return f"${amount:.6f}"
