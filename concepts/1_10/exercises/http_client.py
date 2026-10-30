"""httpx GET with an explicit timeout; parse JSON."""

from __future__ import annotations

from typing import Any

import httpx


def timeout_seconds(client_timeout: httpx.Timeout) -> float:
    """Return the configured connect/read timeout in seconds (use the read value)."""
    raise NotImplementedError


def get_json(client: httpx.Client, path: str) -> dict[str, Any]:
    """GET path, raise_for_status, return response.json()."""
    raise NotImplementedError
