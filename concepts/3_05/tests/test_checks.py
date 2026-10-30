from course_kit.loader import load_concept_module
from docsdesk.models import Incident

checks = load_concept_module("3_05", "checks")


def test_exact() -> None:
    assert checks.grade_exact("Bearer token", "Bearer token") is True
    assert checks.grade_exact("Bearer token", "bearer token") is False


def test_schema() -> None:
    payload = {
        "service": "auth",
        "severity": "high",
        "summary": "token validation failed",
        "timestamp": "2026-10-30T08:00:00Z",
    }
    assert checks.grade_schema(Incident.model_validate, payload) is True
    assert checks.grade_schema(Incident.model_validate, {"service": "auth"}) is False


def test_rubric() -> None:
    text = "Clients send a Bearer token. DocsDesk never logs the token."
    assert checks.grade_rubric(text, ["Bearer", "never"]) is True
    assert checks.grade_rubric(text, ["HMAC"]) is False
