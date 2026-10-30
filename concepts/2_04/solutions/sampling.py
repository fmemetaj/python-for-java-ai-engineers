"""Temperature comparison and FakeLLM determinism (solution)."""

from __future__ import annotations


def is_more_random(temperature_a: float, temperature_b: float) -> bool:
    """True when a is a higher temperature than b."""
    return temperature_a > temperature_b


def fake_is_deterministic() -> bool:
    """Does the course FakeLLM ignore temperature and return scripted text?"""
    return True
