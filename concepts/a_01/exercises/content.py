"""Open: assemble a Responses user content list (text + image)."""

from __future__ import annotations


def text_item(text: str) -> dict[str, str]:
    """type=input_text. Reject blank text."""
    raise NotImplementedError


def vision_content(question: str, fixture_id: str, *, detail: str = "low") -> list[dict[str, str]]:
    """[text_item(question), image_item(fixture_id, detail=detail)]."""
    raise NotImplementedError
