"""Open: classify a snippet as ok / sunset / legacy-0x."""

from __future__ import annotations


def classify(source: str) -> str:
    """'ok', 'sunset' (Assistants/threads), or 'legacy-0x' (ChatCompletion.create)."""
    raise NotImplementedError
