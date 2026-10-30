"""Agent evals for DocsDesk triage: task success and step count.

Graded work uses LLM_PROVIDER=fake. Live OpenAI is optional and is not a
CI gate. A step cap is asserted, not hoped for.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from course_kit.loader import repo_root

from .triage import INCIDENT_REFUND_500, RUNAWAY_INCIDENT, TriageDesk, parse_triage_report

EVAL_FILE = "data/evals/docsdesk_m5.json"


@dataclass
class AgentCaseResult:
    id: str
    passed: bool
    detail: str = ""
    steps: int = 0
    status: str = ""


@dataclass
class AgentEvalReport:
    passed: int
    failed: int
    total: int
    results: list[AgentCaseResult] = field(default_factory=list)
    provider: str = "fake"

    @property
    def ok(self) -> bool:
        return self.failed == 0 and self.total > 0

    def summary(self) -> str:
        return f"agent eval {self.passed}/{self.total} (task success + step count)"


def load_agent_eval_cases(path: Path | None = None) -> list[dict[str, Any]]:
    eval_path = path if path is not None else repo_root() / EVAL_FILE
    payload = json.loads(eval_path.read_text(encoding="utf-8"))
    cases = payload["cases"]
    if not isinstance(cases, list) or not cases:
        raise ValueError("agent eval set must contain cases")
    return cases


def run_agent_eval(*, provider: str | None = None, path: Path | None = None) -> AgentEvalReport:
    name = (provider or os.environ.get("LLM_PROVIDER") or "fake").strip().lower()
    if name != "fake":
        raise RuntimeError("DocsDesk agent evals in this course run with LLM_PROVIDER=fake")
    cases = load_agent_eval_cases(path)
    results: list[AgentCaseResult] = []
    for case in cases:
        results.append(_run_case(case))
    passed = sum(1 for item in results if item.passed)
    return AgentEvalReport(
        passed=passed,
        failed=len(results) - passed,
        total=len(results),
        results=results,
        provider="fake",
    )


def print_report(report: AgentEvalReport) -> None:
    print(report.summary())
    for item in report.results:
        mark = "pass" if item.passed else "fail"
        print(f"  {item.id}: {mark} status={item.status} steps={item.steps} {item.detail}")


def _run_case(case: dict[str, Any]) -> AgentCaseResult:
    case_id = str(case["id"])
    incident = str(case.get("incident") or INCIDENT_REFUND_500)
    max_steps = int(case.get("max_steps", 8))
    approved = bool(case.get("approved", True))
    desk = TriageDesk(max_steps=max_steps, approved=approved)
    try:
        result = desk.investigate(incident, approved=approved)
    finally:
        desk.close()

    expect_status = str(case.get("expect_status", "done"))
    ok = result.status == expect_status
    detail = ""
    if not ok:
        detail = f"expected status {expect_status}"

    expect_steps = case.get("expect_steps")
    if expect_steps is not None and result.steps != int(expect_steps):
        ok = False
        detail = f"expected steps {expect_steps}, got {result.steps}"

    expect_max = case.get("expect_steps_le")
    if expect_max is not None and result.steps > int(expect_max):
        ok = False
        detail = f"steps {result.steps} > {expect_max}"

    must_contain = case.get("must_contain") or []
    blob = result.output_text.lower()
    for needle in must_contain:
        if str(needle).lower() not in blob:
            ok = False
            detail = f"missing {needle!r}"
            break

    if case.get("expect_report"):
        parsed = parse_triage_report(
            result.output_text,
            steps=result.steps,
            approved_write=approved,
        )
        if parsed is None:
            ok = False
            detail = "no TriageReport"
        elif parsed.steps != result.steps:
            ok = False
            detail = "report.steps != loop steps"

    if incident == RUNAWAY_INCIDENT and result.status != "capped":
        ok = False
        detail = "runaway was not capped"

    return AgentCaseResult(
        id=case_id,
        passed=ok,
        detail=detail,
        steps=result.steps,
        status=result.status,
    )
