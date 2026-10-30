"""Guided: build Responses input_image items from fixture ids."""

from __future__ import annotations

from typing import Any


def fixture_image_url(fixture_id: str) -> str:
    """Return fixture://<id>. Reject empty ids."""
    raise NotImplementedError


def image_item(fixture_id: str, *, detail: str = "low") -> dict[str, str]:
    """type=input_image, detail, image_url=fixture://id. detail is low or high."""
    raise NotImplementedError


def parse_fixture_ids(items: list[dict[str, Any]]) -> list[str]:
    """Collect fixture ids from input_image items. Reject non-fixture URLs."""
    raise NotImplementedError
