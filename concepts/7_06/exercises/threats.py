"""Guided: classify a threat and list the capstone rows."""

from __future__ import annotations


def classify_threat(text: str) -> str:
    """Return prompt-injection, data-leakage, excessive-agency, cost-runaway, or other."""
    raise NotImplementedError


def threat_ids() -> list[str]:
    """The five threat ids DocsDesk v1.0 documents."""
    raise NotImplementedError
