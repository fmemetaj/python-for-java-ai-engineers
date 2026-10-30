"""Open: known limitations must mention the fake and no real deploy."""

from __future__ import annotations


def lists_limitations(items: list[str]) -> bool:
    """True when the list mentions the fake and that nothing is deployed."""
    blob = " ".join(items).lower()
    mentions_fake = "fake" in blob
    mentions_no_deploy = "deploy" in blob or "docker" in blob
    return mentions_fake and mentions_no_deploy
