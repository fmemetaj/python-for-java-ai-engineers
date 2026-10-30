"""Patch where the name is looked up; inject a fake getter in tests."""

from __future__ import annotations

from collections.abc import Callable


def lookup_path(owner_module: str, attr: str) -> str:
    """Return 'docsdesk.client.httpx' when client.py does `import httpx`."""
    raise NotImplementedError


def fetch_title(get: Callable[[str], dict[str, str]], url: str) -> str:
    """Call get(url) and return the `title` field."""
    raise NotImplementedError
