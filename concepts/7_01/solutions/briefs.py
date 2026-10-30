"""Guided: the three original capstone briefs."""

from __future__ import annotations

from typing import Any

_BRIEFS: dict[str, dict[str, Any]] = {
    "own-repo": {
        "id": "own-repo",
        "title": "DocsDesk over your public Java repo",
        "corpus": "A public Java/Spring repository you own (README + Javadoc).",
        "write_tools": False,
    },
    "pr-review": {
        "id": "pr-review",
        "title": "PR-review assistant for a Spring project",
        "corpus": "A fixture pull-request diff plus the payments-api docs.",
        "write_tools": True,
    },
    "log-triage": {
        "id": "log-triage",
        "title": "Log-triage assistant",
        "corpus": "Fixture log lines + endpoint specs + the payments-api corpus.",
        "write_tools": True,
    },
}


def list_briefs() -> list[str]:
    """Return the three brief ids in a stable order."""
    return ["own-repo", "pr-review", "log-triage"]


def choose_brief(name: str) -> dict[str, Any]:
    """Return a brief dict with id, title, corpus, write_tools. Raise KeyError if unknown."""
    key = name.strip().lower()
    if key not in _BRIEFS:
        known = ", ".join(list_briefs())
        raise KeyError(f"unknown brief {name!r}. Known: {known}")
    return dict(_BRIEFS[key])
