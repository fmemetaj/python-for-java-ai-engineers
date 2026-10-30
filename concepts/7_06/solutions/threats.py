"""Guided: classify a threat and list the capstone rows."""

from __future__ import annotations


def classify_threat(text: str) -> str:
    """Return prompt-injection, data-leakage, excessive-agency, cost-runaway, or other."""
    lowered = text.lower()
    if "inject" in lowered or "ignore previous" in lowered:
        return "prompt-injection"
    if "secret" in lowered or "api key" in lowered or "leak" in lowered:
        return "data-leakage"
    if "approve" in lowered or "write tool" in lowered or "agency" in lowered:
        return "excessive-agency"
    if "budget" in lowered or "invoice" in lowered or "spend" in lowered:
        return "cost-runaway"
    return "other"


def threat_ids() -> list[str]:
    """The five threat ids DocsDesk v1.0 documents."""
    return [
        "prompt-injection",
        "data-leakage",
        "excessive-agency",
        "cost-runaway",
        "supply-chain",
    ]
