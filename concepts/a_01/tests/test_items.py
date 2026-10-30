import pytest
from course_kit.loader import load_concept_module

items = load_concept_module("a_01", "items")


def test_fixture_url() -> None:
    assert items.fixture_image_url("stacktrace-refund-500") == "fixture://stacktrace-refund-500"


def test_rejects_path() -> None:
    with pytest.raises(ValueError):
        items.fixture_image_url("../secret")


def test_image_item() -> None:
    row = items.image_item("stacktrace-refund-500", detail="high")
    assert row["type"] == "input_image"
    assert row["detail"] == "high"
    assert row["image_url"] == "fixture://stacktrace-refund-500"


def test_parse_ids() -> None:
    ids = items.parse_fixture_ids(
        [
            {"type": "input_text", "text": "why?"},
            {"type": "input_image", "image_url": "fixture://stacktrace-refund-500"},
        ]
    )
    assert ids == ["stacktrace-refund-500"]


def test_parse_rejects_https() -> None:
    with pytest.raises(ValueError):
        items.parse_fixture_ids([{"type": "input_image", "image_url": "https://example.com/x.png"}])
