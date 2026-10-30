"""DocsDesk skeleton: offline HTTP, settings, and secret-redacting logs."""

from __future__ import annotations

import io
import logging

import httpx
import pytest
import respx
from pydantic import SecretStr, ValidationError

from docsdesk.client import DocsClient, fixture_handler
from docsdesk.logging_setup import configure_logging
from docsdesk.models import DocPage
from docsdesk.retry import backoff_seconds, should_retry
from docsdesk.settings import Settings


def test_default_provider_is_fake() -> None:
    settings = Settings.offline()
    assert settings.llm_provider == "fake"


def test_settings_reject_unknown_provider() -> None:
    with pytest.raises(ValidationError):
        Settings.offline(llm_provider="assistants")


def test_secret_str_is_not_in_repr() -> None:
    settings = Settings.offline(openai_api_key=SecretStr("course-test-secret-value"))
    dumped = repr(settings)
    assert "course-test-secret-value" not in dumped


def test_logs_never_contain_secrets() -> None:
    secret = "course-test-secret-value"
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger = configure_logging([secret], handler=handler)
    logger.info("calling provider with %s", secret)
    text = stream.getvalue()
    assert secret not in text
    assert "***" in text


def test_get_page_from_fixture() -> None:
    settings = Settings.offline()
    with DocsClient(settings, sleeper=lambda _delay: None) as client:
        page = client.get_page("auth")
    assert page.slug == "auth"
    assert "Bearer" in page.body
    assert isinstance(page, DocPage)


def test_unknown_page_is_http_error() -> None:
    settings = Settings.offline()
    with DocsClient(settings, sleeper=lambda _delay: None) as client:
        with pytest.raises(httpx.HTTPStatusError):
            client.get_page("missing")


def test_retries_on_500() -> None:
    calls = {"n": 0}

    def flaky(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] < 3:
            return httpx.Response(500, json={"detail": "upstream"})
        return fixture_handler(request)

    settings = Settings.offline(http_retries=3)
    transport = httpx.MockTransport(flaky)
    http = httpx.Client(base_url=settings.docs_base_url, transport=transport, timeout=1.0)
    slept: list[float] = []
    try:
        client = DocsClient(settings, http=http, sleeper=slept.append)
        page = client.get_page("tickets")
    finally:
        http.close()
    assert page.slug == "tickets"
    assert calls["n"] == 3
    assert slept == [backoff_seconds(0, 0.05), backoff_seconds(1, 0.05)]


def test_should_not_retry_ordinary_client_errors() -> None:
    assert should_retry(404) is False
    assert should_retry(400) is False
    assert should_retry(429) is True
    assert should_retry(503) is True


def test_module_entrypoint_runs_offline(capsys: pytest.CaptureFixture[str]) -> None:
    from docsdesk.__main__ import main

    assert main() == 0
    captured = capsys.readouterr()
    assert "tokens in=" in captured.out
    assert "$" in captured.out


def test_session_answers_from_pasted_doc_and_prints_cost() -> None:
    from docsdesk.session import DeskSession

    session = DeskSession("Clients send a Bearer token. DocsDesk never logs the token.")
    turn = session.ask("How do clients authenticate?")
    assert "Bearer" in turn.answer or "token" in turn.answer.lower() or turn.answer
    assert turn.usage.input_tokens > 0
    assert "$" in turn.summary()
    assert "tokens in=" in turn.summary()


def test_session_second_turn_bills_more_input() -> None:
    from docsdesk.session import DeskSession

    session = DeskSession("Tickets are fetched over HTTP with a timeout and retries.")
    first = session.ask("What are tickets?")
    second = session.ask("follow-up")
    assert len(session.turns) == 2
    assert second.usage.input_tokens > first.usage.input_tokens
    assert second.response_id != first.response_id


def test_prompt_file_is_versioned() -> None:
    from docsdesk.session import PROMPT_VERSION, load_instructions

    text = load_instructions()
    assert "DocsDesk" in text
    assert PROMPT_VERSION.startswith("answer_from_doc.")


@respx.mock
def test_respx_can_stub_a_live_looking_url() -> None:
    """WireMock analog: respx intercepts httpx without opening a port."""
    route = respx.get("https://docs.example.test/pages/auth").mock(
        return_value=httpx.Response(
            200,
            json={"slug": "auth", "title": "Authentication", "body": "Bearer token"},
        )
    )
    settings = Settings.offline(docs_base_url="https://docs.example.test")
    http = httpx.Client(base_url=settings.docs_base_url, timeout=1.0)
    try:
        client = DocsClient(settings, http=http, sleeper=lambda _delay: None)
        page = client.get_page("auth")
    finally:
        http.close()
    assert page.title == "Authentication"
    assert route.called
