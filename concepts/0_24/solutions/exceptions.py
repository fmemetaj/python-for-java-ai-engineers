"""EAFP parsing with a dedicated exception type and chaining (solution)."""

from __future__ import annotations


class ParseError(Exception):
    """A log line could not be parsed."""


def parse_level(line: str) -> str:
    """Return the first token. Raise ParseError if the line is blank."""
    text = line.strip()
    if not text:
        raise ParseError("empty line")
    return text.split()[0]


def parse_level_or_default(line: str, default: str = "INFO") -> str:
    """Return parse_level(line), or default when ParseError is raised."""
    try:
        return parse_level(line)
    except ParseError:
        return default


def wrap_parse(line: str) -> str:
    """Call parse_level; on ParseError raise ValueError chained with `from`."""
    try:
        return parse_level(line)
    except ParseError as exc:
        raise ValueError("bad log") from exc
