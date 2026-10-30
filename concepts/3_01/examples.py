"""Structured outputs: Pydantic schema → Responses text.format. Offline."""

from __future__ import annotations

import json

from pydantic import ValidationError

from course_kit.llm import (
    FakeLLM,
    chat_response_format,
    json_schema_from_model,
    responses_create_kwargs,
    responses_text_format,
)
from docsdesk.models import Incident

schema = json_schema_from_model(Incident)
assert schema["additionalProperties"] is False
assert "service" in schema["required"]

text_format = responses_text_format("incident", schema)
assert text_format["type"] == "json_schema"
chat = chat_response_format("incident", schema)
assert "json_schema" in chat

body = responses_create_kwargs(
    model="gpt-4.1-mini",
    instructions="Extract an Incident.",
    input="auth ERROR token validation failed",
    text_format=text_format,
)
assert body["text"] == {"format": text_format}
assert "response_format" not in body
assert "assistant_id" not in body

payload = {
    "service": "auth",
    "severity": "high",
    "summary": "token validation failed for 12 requests",
    "timestamp": "2026-10-30T08:00:00Z",
}
fake = FakeLLM(structured={"extract": payload})
response = fake.complete("extract", text_format=text_format)
assert response.output_parsed == payload
incident = Incident.model_validate(response.output_parsed)
assert incident.service == "auth"

try:
    Incident.model_validate({"service": "auth"})
    raise AssertionError("missing fields must fail")
except ValidationError:
    pass

refused = FakeLLM(refusals=("secrets",)).complete("secrets")
assert refused.refusal

print(json.dumps({"incident": incident.model_dump()}))
print("3.1 examples ok")
