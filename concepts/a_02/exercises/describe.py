"""Guided: look up a vision fixture and build the fake prompt."""

from __future__ import annotations


def fixture_description(fixture_id: str) -> str:
    """Return the catalog description. Unknown ids raise KeyError."""
    raise NotImplementedError


def fake_prompt(fixture_id: str, question: str) -> str:
    """'[image:<id>] <description>\n<question>'."""
    raise NotImplementedError
