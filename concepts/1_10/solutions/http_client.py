"""httpx GET with an explicit timeout; parse JSON (solution)."""

from __future__ import annotations

from typing import Any

import httpx


def timeout_seconds(client_timeout: httpx.Timeout) -> float:
    """Return the configured connect/read timeout in seconds (use the read value)."""
    read = client_timeout.read
    if isinstance(read, (int, float)):
        return float(read)
    raise ValueError("DocsDesk HTTP calls must set a read timeout")


def get_json(client: httpx.Client, path: str) -> dict[str, Any]:
    """GET path, raise_for_status, return response.json()."""
    response = client.get(path)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict):
        raise TypeError("expected a JSON object")
    return payload
