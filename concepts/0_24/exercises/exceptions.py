"""EAFP parsing with a dedicated exception type and chaining."""

from __future__ import annotations


class ParseError(Exception):
    """A log line could not be parsed."""


def parse_level(line: str) -> str:
    """Return the first token. Raise ParseError if the line is blank."""
    raise NotImplementedError


def parse_level_or_default(line: str, default: str = "INFO") -> str:
    """Return parse_level(line), or default when ParseError is raised."""
    raise NotImplementedError


def wrap_parse(line: str) -> str:
    """Call parse_level; on ParseError raise ValueError chained with `from`."""
    raise NotImplementedError
