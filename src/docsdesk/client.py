"""httpx client for the docs service. Default transport is an in-process fixture."""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any
from urllib.parse import urlparse

import httpx

from .models import DocPage, EndpointSpec
from .retry import TransientError, run_with_retry, should_retry
from .settings import Settings

FIXTURE_PAGES: dict[str, dict[str, str]] = {
    "auth": {
        "slug": "auth",
        "title": "Authentication",
        "body": "Clients send a Bearer token. DocsDesk never logs the token.",
    },
    "tickets": {
        "slug": "tickets",
        "title": "Tickets API",
        "body": "GET /tickets/{id} returns a ticket. Timeouts are five seconds.",
    },
    "errors": {
        "slug": "errors",
        "title": "Error codes",
        "body": "401 means missing Bearer token. 429 means backoff and retry.",
    },
    "webhooks": {
        "slug": "webhooks",
        "title": "Webhooks",
        "body": "POST /webhooks registers a URL. Signatures use HMAC.",
    },
}

FIXTURE_ENDPOINTS: dict[str, dict[str, str]] = {
    "GET /tickets/{id}": {
        "method": "GET",
        "path": "/tickets/{id}",
        "summary": "Fetch a ticket by id. Timeouts are five seconds.",
    },
    "POST /tickets": {
        "method": "POST",
        "path": "/tickets",
        "summary": "Create a ticket. Body is JSON with subject and body fields.",
    },
    "GET /pages/{slug}": {
        "method": "GET",
        "path": "/pages/{slug}",
        "summary": "Fetch a docs page by slug from the internal catalog.",
    },
}


def fixture_handler(request: httpx.Request) -> httpx.Response:
    """In-process mock docs service so learners never need a network."""
    slug = request.url.path.rstrip("/").split("/")[-1]
    page = FIXTURE_PAGES.get(slug)
    if page is None:
        return httpx.Response(404, json={"detail": f"unknown page {slug}"})
    return httpx.Response(200, json=page)


def uses_fixture(base_url: str) -> bool:
    host = urlparse(base_url).hostname or ""
    return host.endswith(".internal.test")


def build_http_client(
    settings: Settings,
    *,
    transport: httpx.BaseTransport | None = None,
) -> httpx.Client:
    kwargs: dict[str, Any] = {
        "base_url": settings.docs_base_url,
        "timeout": httpx.Timeout(settings.http_timeout_seconds),
    }
    if transport is not None:
        kwargs["transport"] = transport
    elif uses_fixture(settings.docs_base_url):
        kwargs["transport"] = httpx.MockTransport(fixture_handler)
    return httpx.Client(**kwargs)


class DocsClient:
    """Fetch a DocPage with timeouts and retries. Close via context manager."""

    def __init__(
        self,
        settings: Settings,
        *,
        http: httpx.Client | None = None,
        sleeper: Callable[[float], None] | None = None,
    ) -> None:
        self._settings = settings
        self._owns_http = http is None
        self._http = http if http is not None else build_http_client(settings)
        self._sleeper = sleeper if sleeper is not None else time.sleep

    def close(self) -> None:
        if self._owns_http:
            self._http.close()

    def __enter__(self) -> DocsClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def get_page(self, slug: str) -> DocPage:
        def call() -> DocPage:
            response = self._http.get(f"/pages/{slug}")
            if should_retry(response.status_code):
                raise TransientError(
                    f"transient HTTP {response.status_code}",
                    status_code=response.status_code,
                )
            response.raise_for_status()
            return DocPage.model_validate(response.json())

        return run_with_retry(
            call,
            attempts=self._settings.http_retries,
            sleeper=self._sleeper,
        )

    def search_pages(self, query: str) -> list[DocPage]:
        """Keyword search over the fixture catalog. Empty query is invalid."""
        needle = query.strip().lower()
        if not needle:
            raise ValueError("query must be non-empty")
        hits: list[DocPage] = []
        for page in FIXTURE_PAGES.values():
            blob = f"{page['slug']} {page['title']} {page['body']}".lower()
            if needle in blob:
                hits.append(DocPage.model_validate(page))
        return hits

    def get_endpoint_spec(self, method: str, path: str) -> EndpointSpec:
        key = f"{method.strip().upper()} {path.strip()}"
        spec = FIXTURE_ENDPOINTS.get(key)
        if spec is None:
            raise KeyError(f"unknown endpoint {key}")
        return EndpointSpec.model_validate(spec)
