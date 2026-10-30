"""15-minute Module 0A placement check — 10 small tasks.

Fill each function. Grade with `uv run pytest placement/test_self_check.py`.
NEW-leaning tasks (truthiness, args/kwargs, scope, slicing, generators)
are still worth doing even if you pass them on the first try.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator


def run_mode(module_name: str) -> str:
    """0.1 — 'script' if module_name is __main__, else 'imported'."""
    raise NotImplementedError


def after_rebind(original: list[int]) -> list[int]:
    """0.3 — alias original, rebind the name to [0], return the alias."""
    raise NotImplementedError


def none_label(value: object) -> str:
    """0.4 — 'missing' if value is None, else 'present'."""
    raise NotImplementedError


def keep_truthy(values: list[object]) -> list[object]:
    """0.5 — values that are true in a boolean context."""
    raise NotImplementedError


def label_status(code: int) -> str:
    """0.6 — 200 ok, 400/404 client, 500 server, else other."""
    raise NotImplementedError


def add_tag(tag: str, tags: list[str] | None = None) -> list[str]:
    """0.7 — new list of tags plus tag; no shared default; do not mutate input."""
    raise NotImplementedError


def join_fields(*fields: str, sep: str = ",") -> str:
    """0.8 — join leftover positional fields with sep."""
    raise NotImplementedError


def make_counter(start: int = 0) -> Callable[[], int]:
    """0.9 — closure that increments and returns the enclosed integer."""
    raise NotImplementedError


def error_messages(rows: list[dict[str, object]]) -> list[str]:
    """0.13 — messages of ERROR rows (comprehension)."""
    raise NotImplementedError


def iter_errors(lines: Iterable[str]) -> Iterator[str]:
    """0.14 — yield lines that start with ERROR."""
    raise NotImplementedError
