from typing import Any

import httpx
import pytest
from course_kit.loader import load_concept_module

http_client = load_concept_module("1_10", "http_client")


def _transport(payload: dict[str, Any], status: int = 200) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, json=payload)

    return httpx.MockTransport(handler)


def test_timeout_seconds() -> None:
    timeout = httpx.Timeout(5.0)
    assert http_client.timeout_seconds(timeout) == 5.0


def test_timeout_required() -> None:
    timeout = httpx.Timeout(None)
    with pytest.raises(ValueError):
        http_client.timeout_seconds(timeout)


def test_get_json() -> None:
    transport = _transport({"slug": "auth", "title": "Authentication"})
    with httpx.Client(
        transport=transport, base_url="https://docs.internal.test", timeout=1.0
    ) as client:
        payload = http_client.get_json(client, "/pages/auth")
    assert payload["slug"] == "auth"


def test_get_json_raises_on_404() -> None:
    transport = _transport({"detail": "missing"}, status=404)
    with httpx.Client(
        transport=transport, base_url="https://docs.internal.test", timeout=1.0
    ) as client:
        with pytest.raises(httpx.HTTPStatusError):
            http_client.get_json(client, "/pages/missing")
