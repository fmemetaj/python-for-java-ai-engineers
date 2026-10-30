"""Open: classify a snippet as ok / sunset / legacy-0x."""

from __future__ import annotations

from course_kit.upgrade import scan_source


def classify(source: str) -> str:
    """'ok', 'sunset' (Assistants/threads), or 'legacy-0x' (ChatCompletion.create)."""
    hits = scan_source(source)
    if not hits:
        return "ok"
    if any("Assistants" in item.reason or "threads" in item.reason for item in hits):
        return "sunset"
    return "legacy-0x"
