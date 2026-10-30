import json

import pytest
from pydantic import ValidationError

from course_kit.loader import load_concept_module

schema = load_concept_module("3_01", "schema")

VALID = {
    "service": "auth",
    "severity": "high",
    "summary": "token validation failed for 12 requests",
    "timestamp": "2026-10-30T08:00:00Z",
}


def test_incident_schema_is_strict_object() -> None:
    body = schema.incident_schema()
    assert body["type"] == "object"
    assert body["additionalProperties"] is False
    assert "service" in body["required"]
    assert "severity" in body["properties"]


def test_responses_format_shape() -> None:
    fmt = schema.responses_format(schema.incident_schema())
    assert fmt["type"] == "json_schema"
    assert fmt["name"] == "incident"
    assert fmt["strict"] is True
    assert "json_schema" not in fmt
    assert fmt["schema"]["type"] == "object"


def test_chat_format_is_nested() -> None:
    fmt = schema.chat_format(schema.incident_schema())
    assert fmt["type"] == "json_schema"
    assert "schema" not in fmt
    nested = fmt["json_schema"]
    assert nested["name"] == "incident"
    assert nested["strict"] is True


def test_parse_valid_incident() -> None:
    incident = schema.parse_incident(json.dumps(VALID))
    assert incident.service == "auth"
    assert incident.severity == "high"


def test_parse_missing_field_raises() -> None:
    payload = dict(VALID)
    del payload["summary"]
    with pytest.raises(ValidationError):
        schema.parse_incident(json.dumps(payload))


def test_parse_bad_severity_raises() -> None:
    payload = dict(VALID)
    payload["severity"] = "orange"
    with pytest.raises(ValidationError):
        schema.parse_incident(json.dumps(payload))
