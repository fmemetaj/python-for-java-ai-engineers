"""Screenshot-to-answer on FakeLLM. No pixels, no network."""

from __future__ import annotations

from docsdesk.vision import VisionDesk

desk = VisionDesk()

# Example 1 — catalog description is the only 'pixels' the fake has.
refund = desk.ask_screenshot("stacktrace-refund-500", "Why 500?")
assert refund.fixture_id == "stacktrace-refund-500"
assert "NPE" in refund.answer or "null" in refund.answer.lower()

# Example 2 — request id is present (Module 6 habit).
assert refund.request_id.startswith("req_fake_")

# Example 3 — Responses-shaped content list is attached.
assert refund.items[0]["type"] == "input_text"
assert refund.items[1]["image_url"] == "fixture://stacktrace-refund-500"

# Example 4 — a second screenshot: missing Bearer token.
auth = desk.ask_screenshot("auth-401-screenshot", "Why 401?")
assert "401" in auth.answer or "Bearer" in auth.answer

# Example 5 — the fake cannot teach JPEG artifacts or OCR errors.
print(refund.summary())
print("A.2 examples ok")
