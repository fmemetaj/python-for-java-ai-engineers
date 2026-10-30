"""Guided: look up a vision fixture and build the fake prompt."""

from __future__ import annotations

from course_kit.vision import get_fixture


def fixture_description(fixture_id: str) -> str:
    """Return the catalog description. Unknown ids raise KeyError."""
    return get_fixture(fixture_id).description


def fake_prompt(fixture_id: str, question: str) -> str:
    """'[image:<id>] <description>\n<question>'."""
    if not question.strip():
        raise ValueError("question must be non-empty")
    return f"[image:{fixture_id}] {fixture_description(fixture_id)}\n{question}"
