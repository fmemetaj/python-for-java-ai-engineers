"""Responses image input items from catalog fixtures. Offline."""

from __future__ import annotations

from course_kit.vision import (
    get_fixture,
    input_image_item,
    parse_image_ids,
    responses_image_input,
)

# Example 1 — a fixture id is not a URL fetch.
fixture = get_fixture("stacktrace-refund-500")
assert fixture.width == 1024
assert "NullPointerException" in fixture.description

# Example 2 — Responses item type is input_image.
item = input_image_item("stacktrace-refund-500", detail="low")
assert item["type"] == "input_image"
assert item["image_url"] == "fixture://stacktrace-refund-500"

# Example 3 — user content is text then image.
content = responses_image_input("Why 500?", "stacktrace-refund-500")
assert content[0]["type"] == "input_text"
assert parse_image_ids(content) == ["stacktrace-refund-500"]

# Example 4 — https URLs are rejected in graded helpers.
try:
    parse_image_ids([{"type": "input_image", "image_url": "https://example.com/x.png"}])
    raise AssertionError("https must be rejected")
except ValueError:
    pass

# Example 5 — a second fixture exists for auth 401.
auth = get_fixture("auth-401-screenshot")
assert "401" in auth.description

print("A.1 examples ok")
