"""Guided: run a prefix of priced calls under a USD cap."""

from __future__ import annotations

from course_kit.upgrade import SmokeCall, SmokeReport


def capped(calls: list[SmokeCall], cap_usd: float) -> SmokeReport:
    """Run while spent + next cost stays <= cap. Skip the rest."""
    raise NotImplementedError
