"""Guided: lockfile equality and changelog actions."""

from __future__ import annotations

from course_kit.upgrade import ChangelogEntry, pin_ok, requires_responses


def pin_matches(declared: str, locked: str) -> bool:
    """True when both non-empty strings are equal."""
    return pin_ok(declared, locked)


def needs_responses(entry: ChangelogEntry) -> bool:
    """True when the action mentions responses or the kind is sunset."""
    return requires_responses(entry)
