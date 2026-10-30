"""Open: assemble a Responses user content list (text + image)."""

from __future__ import annotations

from course_kit.vision import input_image_item


def text_item(text: str) -> dict[str, str]:
    """type=input_text. Reject blank text."""
    if not text.strip():
        raise ValueError("text must be non-empty")
    return {"type": "input_text", "text": text}


def vision_content(question: str, fixture_id: str, *, detail: str = "low") -> list[dict[str, str]]:
    """[text_item(question), image_item(fixture_id, detail=detail)]."""
    return [text_item(question), input_image_item(fixture_id, detail=detail)]
