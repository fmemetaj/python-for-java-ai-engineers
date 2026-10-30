"""Portfolio README sections, demo length, and the self-assessment list."""

from __future__ import annotations


def readme_sections() -> list[str]:
    """Sections a hiring manager should find, in a stable order."""
    raise NotImplementedError


def demo_minutes() -> int:
    """How long the walkthrough is, in minutes."""
    raise NotImplementedError


def self_assessment_items() -> list[str]:
    """Checklist lines the learner ticks before showing the repo."""
    raise NotImplementedError
