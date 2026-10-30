"""Open: run VisionDesk on a fixture screenshot (FakeLLM)."""

from __future__ import annotations

from docsdesk.vision import VisionAnswer, VisionDesk


def ask_refund_stacktrace() -> VisionAnswer:
    """Ask why the refund screenshot is HTTP 500. Use VisionDesk()."""
    desk = VisionDesk()
    return desk.ask_screenshot(
        "stacktrace-refund-500",
        "Why did this refund return HTTP 500?",
    )


def mentions_npe(answer: str) -> bool:
    """True when the answer mentions NullPointer or NPE (case-insensitive)."""
    lowered = answer.lower()
    return "nullpointer" in lowered or "npe" in lowered
