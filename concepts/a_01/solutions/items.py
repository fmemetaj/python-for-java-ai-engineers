"""Guided: build Responses input_image items from fixture ids."""

from __future__ import annotations

from typing import Any


def fixture_image_url(fixture_id: str) -> str:
    """Return fixture://<id>. Reject empty ids."""
    if not fixture_id or "/" in fixture_id or "\\" in fixture_id:
        raise ValueError("fixture_id must be a simple catalog key")
    return f"fixture://{fixture_id}"


def image_item(fixture_id: str, *, detail: str = "low") -> dict[str, str]:
    """type=input_image, detail, image_url=fixture://id. detail is low or high."""
    if detail not in {"low", "high"}:
        raise ValueError("detail must be 'low' or 'high'")
    return {
        "type": "input_image",
        "detail": detail,
        "image_url": fixture_image_url(fixture_id),
    }


def parse_fixture_ids(items: list[dict[str, Any]]) -> list[str]:
    """Collect fixture ids from input_image items. Reject non-fixture URLs."""
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
    return ids
