"""Migrate a Chat Completions request dict to Responses (solution)."""

from __future__ import annotations

from course_kit.llm.migrate import migrate_chat_body_to_responses as _migrate


def migrate_chat_body_to_responses(chat_body: dict[str, object]) -> dict[str, object]:
    """Map messages → input + instructions. Map response_format → text.format."""
    return _migrate(chat_body)
