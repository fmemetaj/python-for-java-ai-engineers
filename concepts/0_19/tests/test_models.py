import pytest
from pydantic import ValidationError
from course_kit.loader import load_concept_module

models = load_concept_module("0_19", "models")


def test_parse_log_line() -> None:
    parsed = models.parse_log_line("ERROR disk full")
    assert parsed == models.LogLine(level="ERROR", message="disk full")
    assert models.parse_log_line("  ") is None


def test_frozen_dataclass() -> None:
    line = models.LogLine("INFO", "ok")
    with pytest.raises(Exception):
        line.level = "ERROR"  # type: ignore[misc]


def test_pydantic_accepts_and_rejects() -> None:
    ticket = models.parse_ticket({"id": 1, "subject": "Login"})
    assert ticket.id == 1
    with pytest.raises(ValidationError):
        models.parse_ticket({"id": 0, "subject": "Login"})
    with pytest.raises(ValidationError):
        models.parse_ticket({"id": 1, "subject": "x"})
