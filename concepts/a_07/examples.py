"""Pin the SDK, read a fake changelog. Offline."""

from __future__ import annotations

from course_kit.upgrade import ChangelogEntry, load_changelog, pin_ok, requires_responses

# Example 1 — lockfile equality is the Maven-enforced version analog.
assert pin_ok("3.41.0", "3.41.0") is True
assert pin_ok("3.41.0", "3.40.0") is False

# Example 2 — the fixture changelog is dated and local.
entries = load_changelog()
assert entries[0].date == "2026-08-26"
assert entries[0].kind == "sunset"

# Example 3 — sunset rows tell you to use Responses.
assert requires_responses(entries[0]) is True

# Example 4 — a note that does not mention responses is not a migration trigger.
note = ChangelogEntry("2026-01-01", "note", "typo", "fix docs")
assert requires_responses(note) is False

# Example 5 — CI uses uv sync --locked; drifting pins fail the build.
print(entries[0].summary)
print("A.7 examples ok")
