"""Scan a snippet for sunset APIs. Offline string matching."""

from __future__ import annotations

from course_kit.upgrade import scan_source, sunset_free

# Example 1 — Responses is clean.
assert sunset_free("client.responses.create(input='hi')") is True

# Example 2 — 0.x helper is flagged.
hits = scan_source("openai.ChatCompletion.create(model='x')")
assert hits[0].pattern == "openai.ChatCompletion.create"

# Example 3 — Assistants / threads are sunset.
assert scan_source("client.beta.threads.create()")[0].line == 1

# Example 4 — current Chat Completions is still supported (Module 2 taught it).
assert sunset_free("client.chat.completions.create(messages=[])") is True

# Example 5 — the scanner cannot teach a live SDK migration; it catches strings.
print([item.reason for item in hits])
print("A.8 examples ok")
