"""Offline eval harness for DocsDesk v0.3. Graded work uses LLM_PROVIDER=fake.

Live OpenAI is optional: the pass rate is reported with no threshold claimed.
Checks: exact JSON, Pydantic schema, rubric (substring), invalid tool args.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from course_kit.loader import repo_root
from course_kit.llm.schema import json_schema_from_model

from .assistant import DocsDesk, scripted_docsdesk_llm
from .models import Incident, TypedAnswer
from .tools import ToolBlockedError, ToolRunner, validate_args

EVAL_FILE = "data/evals/docsdesk_m3.json"


@dataclass
class CaseResult:
    id: str
    passed: bool
    check: str
    detail: str = ""


@dataclass
class EvalReport:
    passed: int
    failed: int
    total: int
    results: list[CaseResult] = field(default_factory=list)
    provider: str = "fake"

    @property
    def rate(self) -> float:
        return self.passed / self.total if self.total else 0.0

    def summary(self) -> str:
        if self.provider == "fake":
            return f"fake {self.passed}/{self.total} (CI gate)"
        return format_live_rate(self.passed, self.total)


def format_live_rate(passed: int, total: int) -> str:
    """Live runs report a rate only — no pass/fail threshold is claimed."""
    return f"live pass rate {passed}/{total} (no threshold claimed)"


def load_eval_cases(path: Path | None = None) -> list[dict[str, Any]]:
    eval_path = path if path is not None else repo_root() / EVAL_FILE
    payload = json.loads(eval_path.read_text(encoding="utf-8"))
    cases = payload["cases"]
    if not isinstance(cases, list) or len(cases) < 15:
        raise ValueError("eval set must contain at least 15 cases")
    return cases


def exact_match(expected: object, actual: object) -> bool:
    return expected == actual


def schema_ok(model_name: str, payload: object) -> bool:
    models = {"Incident": Incident, "TypedAnswer": TypedAnswer}
    model = models[model_name]
    if isinstance(payload, str):
        model.model_validate_json(payload)
    else:
        model.model_validate(payload)
    return True


def rubric_contains(text: str, needles: list[str]) -> bool:
    lowered = text.lower()
    return all(needle.lower() in lowered for needle in needles)


def _run_case(case: dict[str, Any], desk: DocsDesk, runner: ToolRunner) -> CaseResult:
    case_id = str(case["id"])
    kind = str(case["check"])
    try:
        if kind == "exact":
            answer = desk.ask(str(case["prompt"]))
            ok = exact_match(case["expected_answer"], answer.answer)
            return CaseResult(case_id, ok, kind, answer.answer)
        if kind == "schema":
            schema_ok(str(case["model"]), case["payload"])
            _ = json_schema_from_model(Incident if case["model"] == "Incident" else TypedAnswer)
            return CaseResult(case_id, True, kind)
        if kind == "rubric":
            answer = desk.ask(str(case["prompt"]))
            needles = [str(item) for item in case["contains"]]
            ok = rubric_contains(answer.answer, needles)
            return CaseResult(case_id, ok, kind, answer.answer)
        if kind == "invalid_args":
            raised = False
            try:
                validate_args(str(case["tool"]), case["arguments"])
            except (ValidationError, ValueError):
                raised = True
            return CaseResult(case_id, raised, kind)
        if kind == "blocked":
            raised = False
            try:
                runner.invoke(str(case["tool"]), case.get("arguments") or {})
            except ToolBlockedError:
                raised = True
            return CaseResult(case_id, raised, kind)
        if kind == "tool":
            answer = desk.ask(str(case["prompt"]))
            needles = [str(item) for item in case["contains"]]
            ok = rubric_contains(answer.answer, needles) and len(answer.citations) >= 1
            return CaseResult(case_id, ok, kind, answer.answer)
        return CaseResult(case_id, False, kind, f"unknown check {kind}")
    except Exception as exc:  # noqa: BLE001 — eval cases must not crash the harness
        return CaseResult(case_id, False, kind, f"{type(exc).__name__}: {exc}")


def run_docsdesk_eval(
    *,
    provider: str | None = None,
    cases: list[dict[str, Any]] | None = None,
) -> EvalReport:
    """Run a golden set (default: committed Module 3 file). Graded CI uses fake only."""
    name = (provider or os.environ.get("LLM_PROVIDER") or "fake").strip().lower() or "fake"
    if name != "fake":
        raise RuntimeError(
            "Live eval is optional. Keep LLM_PROVIDER=fake for graded work. "
            "If you opt in locally, format_live_rate(passed, total) reports the "
            "rate with no threshold claimed. Never commit keys."
        )
    loaded = cases if cases is not None else load_eval_cases()
    llm = scripted_docsdesk_llm()
    with DocsDesk(client=llm) as desk, ToolRunner() as runner:
        results = [_run_case(case, desk, runner) for case in loaded]
    passed = sum(1 for item in results if item.passed)
    failed = len(results) - passed
    return EvalReport(
        passed=passed,
        failed=failed,
        total=len(results),
        results=results,
        provider="fake",
    )


def parse_typed_or_none(response_text: str) -> TypedAnswer | None:
    try:
        return TypedAnswer.model_validate_json(response_text)
    except ValidationError:
        return None


__all__ = [
    "CaseResult",
    "EvalReport",
    "exact_match",
    "format_live_rate",
    "load_eval_cases",
    "parse_typed_or_none",
    "rubric_contains",
    "run_docsdesk_eval",
    "schema_ok",
]
