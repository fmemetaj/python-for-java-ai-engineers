"""DocsDesk triage mode: 5-step fake trajectory, approval, step cap, evals."""

from __future__ import annotations

import os

import pytest

from docsdesk.agent_eval import run_agent_eval
from docsdesk.triage import INCIDENT_REFUND_500, RUNAWAY_INCIDENT, TriageDesk, parse_triage_report


def test_five_step_refund_trajectory() -> None:
    with TriageDesk(approved=True) as desk:
        result = desk.investigate(INCIDENT_REFUND_500, approved=True)
    assert result.status == "done"
    assert result.steps == 5
    assert result.tool_names == [
        "search_docs",
        "get_endpoint_spec",
        "search_corpus",
        "propose_page",
    ]
    report = parse_triage_report(result.output_text, steps=result.steps, approved_write=True)
    assert report is not None
    assert report.steps == 5
    assert "RefundService" in report.root_cause
    kinds = [span.kind for span in result.trace.spans]
    assert "agent" in kinds or result.trace.as_list()[0]["kind"] == "agent"


def test_approval_gate_blocks_write() -> None:
    with TriageDesk(approved=False) as desk:
        result = desk.investigate(INCIDENT_REFUND_500, approved=False)
    assert result.status == "denied"
    assert result.steps == 4
    assert result.tool_names[-1] == "propose_page"
    assert result.output_text == ""


def test_step_cap_enforced() -> None:
    with TriageDesk(max_steps=3, approved=True) as desk:
        result = desk.investigate(RUNAWAY_INCIDENT, approved=True)
    assert result.status == "capped"
    assert result.steps == 3


def test_agent_eval_gate() -> None:
    report = run_agent_eval(provider="fake")
    failed = [item.id for item in report.results if not item.passed]
    assert report.ok, failed
    assert report.total == 4


def test_live_provider_is_opt_in() -> None:
    previous = os.environ.get("LLM_PROVIDER")
    os.environ["LLM_PROVIDER"] = "openai"
    try:
        with pytest.raises(RuntimeError, match="fake"):
            run_agent_eval()
    finally:
        if previous is None:
            os.environ.pop("LLM_PROVIDER", None)
        else:
            os.environ["LLM_PROVIDER"] = previous


def test_triage_and_eval_agent_entrypoints(capsys: pytest.CaptureFixture[str]) -> None:
    from docsdesk.__main__ import main

    assert main(["triage"]) == 0
    captured = capsys.readouterr()
    assert "status=done" in captured.out
    assert "steps=5" in captured.out

    assert main(["eval-agent"]) == 0
    captured = capsys.readouterr()
    assert "agent eval" in captured.out
