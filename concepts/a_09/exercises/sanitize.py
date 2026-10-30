"""Open: redact secrets from a recorded JSON object."""

from __future__ import annotations

from typing import Any


def sanitize(payload: dict[str, Any]) -> dict[str, Any]:
    """Replace sk-..., Bearer tokens, and course-test-secret-value with ***."""
    raise NotImplementedError
