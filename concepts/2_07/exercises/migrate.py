"""Migrate a Chat Completions request dict to Responses."""

from __future__ import annotations


def migrate_chat_body_to_responses(chat_body: dict[str, object]) -> dict[str, object]:
    """Map messages → input + instructions. Map response_format → text.format.

    Reject assistant_id (Assistants API sunset 2026-08-26). Set store False.
    """
    raise NotImplementedError
