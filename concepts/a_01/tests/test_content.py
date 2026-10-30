import pytest
from course_kit.loader import load_concept_module

content = load_concept_module("a_01", "content")


def test_vision_content_order() -> None:
    rows = content.vision_content("Why 500?", "stacktrace-refund-500")
    assert rows[0]["type"] == "input_text"
    assert rows[0]["text"] == "Why 500?"
    assert rows[1]["type"] == "input_image"
    assert rows[1]["image_url"].startswith("fixture://")


def test_blank_text_rejected() -> None:
    with pytest.raises(ValueError):
        content.text_item("   ")
