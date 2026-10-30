import pytest
from course_kit.loader import load_concept_module

service = load_concept_module("6_06", "service")


def test_health() -> None:
    body = service.health()
    assert body["status"] == "ok"
    assert body["provider"] == "fake"


def test_validate_question() -> None:
    assert service.validate_question("  hello  ") == "hello"
    with pytest.raises(ValueError):
        service.validate_question("   ")
    with pytest.raises(ValueError):
        service.validate_question("")
