"""DocsDesk v0.3 eval set: ≥15 cases, all offline on FakeLLM."""

from __future__ import annotations

import os

import pytest
from pydantic import ValidationError

from docsdesk.evals import format_live_rate, load_eval_cases, run_docsdesk_eval
from docsdesk.tools import ToolRunner, validate_args


def test_eval_file_has_at_least_fifteen_cases() -> None:
    cases = load_eval_cases()
    assert len(cases) >= 15


def test_fake_eval_all_pass() -> None:
    report = run_docsdesk_eval(provider="fake")
    failed_ids = [item.id for item in report.results if not item.passed]
    assert failed_ids == []
    assert report.passed == report.total
    assert report.total >= 15
    assert "CI gate" in report.summary()


def test_live_provider_is_opt_in() -> None:
    previous = os.environ.get("LLM_PROVIDER")
    os.environ["LLM_PROVIDER"] = "openai"
    try:
        with pytest.raises(RuntimeError, match="no threshold"):
            run_docsdesk_eval()
    finally:
        if previous is None:
            os.environ.pop("LLM_PROVIDER", None)
        else:
            os.environ["LLM_PROVIDER"] = previous


def test_live_rate_copy() -> None:
    line = format_live_rate(12, 15)
    assert "12/15" in line
    assert "no threshold claimed" in line


def test_scripted_invalid_args_fail_validation() -> None:
    with pytest.raises(ValidationError):
        validate_args("search_docs", {"query": 1})
    with ToolRunner() as runner:
        payload = runner.invoke_handled("search_docs", '{"query":1}')
    assert "error" in payload
