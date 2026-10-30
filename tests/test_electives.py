"""Library tests for vision, hosted-tool, and upgrade electives."""

from __future__ import annotations

import pytest

from course_kit.hosted import choose_stack, next_hosted_turn, overlap_rate
from course_kit.upgrade import (
    SmokeCall,
    load_changelog,
    run_smoke,
    sanitize_record,
    scan_source,
    sunset_free,
)
from course_kit.vision import (
    get_fixture,
    image_cost_usd,
    image_token_count,
    parse_image_ids,
    responses_image_input,
)


def test_vision_fixture_and_items() -> None:
    fixture = get_fixture("stacktrace-refund-500")
    assert fixture.width == 1024
    items = responses_image_input("Why 500?", fixture.id)
    assert parse_image_ids(items) == [fixture.id]
    with pytest.raises(ValueError):
        parse_image_ids([{"type": "input_image", "image_url": "https://example.com/x.png"}])


def test_image_tokens_low_and_high() -> None:
    assert image_token_count("low", 4000, 3000) == 85
    assert image_token_count("high", 1024, 768) == 765
    amount = image_cost_usd(
        image_tokens=85,
        text_input_tokens=0,
        output_tokens=10,
        input_per_million=0.40,
        output_per_million=1.60,
    )
    assert abs(amount - (85 * 0.40 + 10 * 1.60) / 1_000_000) < 1e-12


def test_choose_stack_prefers_own() -> None:
    assert overlap_rate(["a"], ["b"]) == 0.0
    own = choose_stack(
        own_recall=0.8,
        hosted_available=True,
        can_export=True,
        can_eval=True,
        overlap=0.1,
    )
    assert own.choice == "own"
    hosted = choose_stack(
        own_recall=0.0,
        hosted_available=True,
        can_export=False,
        can_eval=False,
        overlap=0.0,
    )
    assert hosted.choice == "hosted"


def test_hosted_loop_caps() -> None:
    tool = next_hosted_turn(0, "q", [])
    assert tool.kind == "tool"
    with pytest.raises(ValueError):
        next_hosted_turn(2, "q", [])


def test_changelog_and_scanner() -> None:
    entries = load_changelog()
    assert any(item.kind == "sunset" for item in entries)
    assert sunset_free("client.responses.create()") is True
    assert scan_source("openai.ChatCompletion.create()")
    assert sunset_free("client.chat.completions.create()") is True


def test_smoke_cap_and_sanitize() -> None:
    report = run_smoke(
        [SmokeCall("a", 0.004), SmokeCall("b", 0.004), SmokeCall("c", 0.004)],
        0.01,
    )
    assert report.ran == ("a", "b")
    assert report.skipped == ("c",)
    cleaned = sanitize_record({"token": "sk-abcdefghijklmnop", "ok": 1})
    assert cleaned["token"] == "***"
    assert cleaned["ok"] == 1
