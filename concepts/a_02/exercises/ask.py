"""Open: run VisionDesk on a fixture screenshot (FakeLLM)."""

from __future__ import annotations

from docsdesk.vision import VisionAnswer


def ask_refund_stacktrace() -> VisionAnswer:
    """Ask why the refund screenshot is HTTP 500. Use VisionDesk()."""
    raise NotImplementedError


def mentions_npe(answer: str) -> bool:
    """True when the answer mentions NullPointer or NPE (case-insensitive)."""
    raise NotImplementedError
