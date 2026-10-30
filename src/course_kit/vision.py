"""Vision inputs for the Responses API — fixture images, never live pixels.

Official docs: https://platform.openai.com/docs/guides/images-vision
Input shape: https://platform.openai.com/docs/guides/migrate-to-responses

Graded work uses named fixtures (`fixture://id`). The fake cannot see real
pixels; it returns the catalog description. Live `image_url` fetches are
optional and never used in CI.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .loader import repo_root

FIXTURES_PATH = Path("data") / "fixtures" / "vision.json"

# Published vision token counts (OpenAI images guide, retrieved 2026-10-30).
LOW_DETAIL_TOKENS = 85
HIGH_DETAIL_BASE_TOKENS = 85
HIGH_DETAIL_TILE_TOKENS = 170
TILE_PX = 512
MAX_SIDE_PX = 2048
SHORT_SIDE_PX = 768


@dataclass(frozen=True)
class VisionFixture:
    id: str
    alt: str
    description: str
    width: int
    height: int
    answer: str


def load_vision_fixtures(path: Path | None = None) -> dict[str, VisionFixture]:
    json_path = path if path is not None else repo_root() / FIXTURES_PATH
    raw = json.loads(json_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("vision fixtures must be a JSON object")
    out: dict[str, VisionFixture] = {}
    for fixture_id, row in raw.items():
        if not isinstance(row, dict):
            raise ValueError(f"fixture {fixture_id!r} must be an object")
        out[str(fixture_id)] = VisionFixture(
            id=str(fixture_id),
            alt=str(row["alt"]),
            description=str(row["description"]),
            width=int(row["width"]),
            height=int(row["height"]),
            answer=str(row["answer"]),
        )
    return out


def get_fixture(fixture_id: str, table: dict[str, VisionFixture] | None = None) -> VisionFixture:
    fixtures = table if table is not None else load_vision_fixtures()
    try:
        return fixtures[fixture_id]
    except KeyError as exc:
        known = ", ".join(sorted(fixtures))
        raise KeyError(f"Unknown vision fixture {fixture_id!r}. Known: {known}") from exc


def input_image_item(fixture_id: str, *, detail: str = "low") -> dict[str, str]:
    """Responses `input_image` item. URL is a fixture scheme, not a fetch."""
    if detail not in {"low", "high"}:
        raise ValueError("detail must be 'low' or 'high'")
    get_fixture(fixture_id)
    return {
        "type": "input_image",
        "detail": detail,
        "image_url": f"fixture://{fixture_id}",
    }


def input_text_item(text: str) -> dict[str, str]:
    if not text.strip():
        raise ValueError("text must be non-empty")
    return {"type": "input_text", "text": text}


def responses_image_input(
    question: str,
    fixture_id: str,
    *,
    detail: str = "low",
) -> list[dict[str, str]]:
    """User content list for `client.responses.create(..., input=[...])`."""
    return [
        input_text_item(question),
        input_image_item(fixture_id, detail=detail),
    ]


def parse_image_ids(items: list[dict[str, Any]]) -> list[str]:
    """Collect fixture ids from Responses-shaped input content items."""
    ids: list[str] = []
    for item in items:
        if item.get("type") != "input_image":
            continue
        url = str(item.get("image_url") or "")
        if not url.startswith("fixture://"):
            raise ValueError("graded work only accepts fixture:// image URLs")
        ids.append(url.removeprefix("fixture://"))
    if not ids:
        raise ValueError("no input_image items")
    for fixture_id in ids:
        get_fixture(fixture_id)
    return ids


def image_token_count(detail: str, width: int, height: int) -> int:
    """Approximate published vision token counts. Not a live tokenizer.

    low: 85 tokens. high: scale to 2048, then shortest side 768, then
    512px tiles at 170 tokens each plus an 85-token base.
    """
    if detail == "low":
        return LOW_DETAIL_TOKENS
    if detail != "high":
        raise ValueError("detail must be 'low' or 'high'")
    if width < 1 or height < 1:
        raise ValueError("width and height must be >= 1")
    scaled_w, scaled_h = float(width), float(height)
    longest = max(scaled_w, scaled_h)
    if longest > MAX_SIDE_PX:
        scale = MAX_SIDE_PX / longest
        scaled_w *= scale
        scaled_h *= scale
    shortest = min(scaled_w, scaled_h)
    if shortest > SHORT_SIDE_PX:
        scale = SHORT_SIDE_PX / shortest
        scaled_w *= scale
        scaled_h *= scale
    tiles = math.ceil(scaled_w / TILE_PX) * math.ceil(scaled_h / TILE_PX)
    return HIGH_DETAIL_BASE_TOKENS + HIGH_DETAIL_TILE_TOKENS * tiles


def image_cost_usd(
    *,
    image_tokens: int,
    text_input_tokens: int,
    output_tokens: int,
    input_per_million: float,
    output_per_million: float,
    unit_tokens: int = 1_000_000,
) -> float:
    """Images bill as input tokens at the model input rate."""
    if min(image_tokens, text_input_tokens, output_tokens) < 0:
        raise ValueError("token counts must be >= 0")
    if unit_tokens <= 0:
        raise ValueError("unit_tokens must be > 0")
    million = float(unit_tokens)
    return (
        image_tokens + text_input_tokens
    ) * input_per_million / million + output_tokens * output_per_million / million
