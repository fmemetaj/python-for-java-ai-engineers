"""DocsDesk elective extras: vision, hosted compare, spend-capped smoke."""

from __future__ import annotations

from docsdesk.hosted import compare_retrieve
from docsdesk.smoke import run_elective_smoke
from docsdesk.vision import VisionDesk


def test_vision_refund_screenshot() -> None:
    desk = VisionDesk()
    result = desk.ask_screenshot(
        "stacktrace-refund-500",
        "Why did this refund return HTTP 500?",
    )
    assert result.fixture_id == "stacktrace-refund-500"
    assert result.request_id
    assert result.image_tokens == 85
    assert "NPE" in result.answer or "null" in result.answer.lower()
    assert result.items[1]["type"] == "input_image"


def test_hosted_compare_stays_on_own() -> None:
    comparison = compare_retrieve("How do I refund a captured payment?")
    assert comparison.decision.choice == "own"
    assert comparison.hosted_ids
    assert comparison.record["assistants"] is False
    assert comparison.record["api"] == "responses"


def test_smoke_is_fake_and_capped() -> None:
    result = run_elective_smoke(cap_usd=0.01)
    assert result.report.within_budget is True
    assert result.fixture["provider"] == "fake"
    assert "sk-" not in str(result.fixture)
