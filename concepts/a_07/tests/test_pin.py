import pytest
from course_kit.loader import load_concept_module
from course_kit.upgrade import ChangelogEntry, load_changelog

pin = load_concept_module("a_07", "pin")


def test_pin_matches() -> None:
    assert pin.pin_matches("3.41.0", "3.41.0") is True
    assert pin.pin_matches("3.41.0", "3.40.0") is False


def test_empty_rejected() -> None:
    with pytest.raises(ValueError):
        pin.pin_matches("", "3.41.0")


def test_sunset_needs_responses() -> None:
    entries = load_changelog()
    sunset = next(item for item in entries if item.kind == "sunset")
    assert pin.needs_responses(sunset) is True
    recommend = ChangelogEntry("2025-01-01", "note", "n", "keep tests green")
    assert pin.needs_responses(recommend) is False
