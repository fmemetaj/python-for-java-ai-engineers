"""15-minute Module 0A placement check (solution)."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator


def run_mode(module_name: str) -> str:
    """0.1 — 'script' if module_name is __main__, else 'imported'."""
    return "script" if module_name == "__main__" else "imported"


def after_rebind(original: list[int]) -> list[int]:
    """0.3 — alias original, rebind the name to [0], return the alias."""
    alias = original
    original = [0]
    assert original == [0]
    return alias


def none_label(value: object) -> str:
    """0.4 — 'missing' if value is None, else 'present'."""
    return "missing" if value is None else "present"


def keep_truthy(values: list[object]) -> list[object]:
    """0.5 — values that are true in a boolean context."""
    return [value for value in values if value]


def label_status(code: int) -> str:
    """0.6 — 200 ok, 400/404 client, 500 server, else other."""
    if code == 200:
        return "ok"
    if code in {400, 404}:
        return "client"
    if code == 500:
        return "server"
    return "other"


def add_tag(tag: str, tags: list[str] | None = None) -> list[str]:
    """0.7 — new list of tags plus tag; no shared default; do not mutate input."""
    collected = [] if tags is None else list(tags)
    collected.append(tag)
    return collected


def join_fields(*fields: str, sep: str = ",") -> str:
    """0.8 — join leftover positional fields with sep."""
    return sep.join(fields)


def make_counter(start: int = 0) -> Callable[[], int]:
    """0.9 — closure that increments and returns the enclosed integer."""
    n = start

    def inc() -> int:
        nonlocal n
        n += 1
        return n

    return inc


def error_messages(rows: list[dict[str, object]]) -> list[str]:
    """0.13 — messages of ERROR rows (comprehension)."""
    return [str(row["message"]) for row in rows if row["level"] == "ERROR"]


def iter_errors(lines: Iterable[str]) -> Iterator[str]:
    """0.14 — yield lines that start with ERROR."""
    for line in lines:
        if line.startswith("ERROR"):
            yield line
