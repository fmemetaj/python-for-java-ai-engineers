"""Sync and async httpx against an in-process mock — no network."""

from __future__ import annotations

import asyncio

import httpx


def handler(request: httpx.Request) -> httpx.Response:
    return httpx.Response(200, json={"slug": "auth", "title": "Authentication"})


def sync_get() -> dict[str, str]:
    transport = httpx.MockTransport(handler)
    with httpx.Client(
        transport=transport, base_url="https://docs.internal.test", timeout=1.0
    ) as client:
        response = client.get("/pages/auth")
        payload = response.json()
        assert isinstance(payload, dict)
        return {"slug": str(payload["slug"]), "title": str(payload["title"])}


async def async_get() -> str:
    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(
        transport=transport, base_url="https://docs.internal.test", timeout=1.0
    ) as client:
        response = await client.get("/pages/auth")
        payload = response.json()
        return str(payload["title"])


assert sync_get()["slug"] == "auth"
assert asyncio.run(async_get()) == "Authentication"
print("1.10 examples ok")
