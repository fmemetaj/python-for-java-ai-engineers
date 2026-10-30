"""Observability: request ids, JSON logs, spans. Offline FakeLLM."""

from __future__ import annotations

import json

from course_kit.llm import FakeLLM
from docsdesk.observe import (
    bind_from_response,
    current_request_id,
    format_json_log,
    pick_request_id,
    span_ms,
    start_span,
)
from docsdesk.production import ProductionDesk

# Example 1 — SDK HTTP id wins over a local fallback.
assert pick_request_id("req_fake_0001", "req_local") == "req_fake_0001"
assert pick_request_id("", "req_local") == "req_local"

# Example 2 — FakeLLM fills request_id (not the same as response.id).
response = FakeLLM(script={"ping": "pong"}).complete("ping")
assert response.request_id.startswith("req_fake_")
assert response.id.startswith("resp_fake_")
assert response.id != response.request_id
bind_from_response(response)
assert current_request_id() == response.request_id

# Example 3 — JSON log line carries request_id and cost_usd.
line = format_json_log("docsdesk.ask", cost_usd=0.00004, cached=False)
payload = json.loads(line)
assert payload["event"] == "docsdesk.ask"
assert payload["request_id"] == response.request_id
assert payload["cost_usd"] == 0.00004

# Example 4 — span duration is non-negative.
assert span_ms(10.0, 25.0) == 15.0
with start_span("docsdesk.ask") as span:
    pass
assert span.duration_ms >= 0.0
assert span.name == "docsdesk.ask"

# Example 5 — ProductionDesk logs cost on a real ask.
with ProductionDesk() as desk:
    result = desk.ask("How do clients authenticate?")
assert "Bearer" in result.answer
assert "cost_usd" in result.log_line
assert result.request_id

print(result.log_line)
print("6.2 examples ok")
