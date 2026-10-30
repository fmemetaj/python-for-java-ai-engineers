"""DocsDesk triage mode: a multi-step investigation with an approval gate.

Offline: FakeLLM trajectories + fixture tools. A 5-step refund-500 script
is the graded path. propose_page is simulated (would_write); nothing is
sent or written. Generation uses Responses-shaped complete(), never Assistants.
"""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import ValidationError

from course_kit.agent import AgentMemory, AgentResult, AgentTrace, run_agent_loop
from course_kit.llm import FakeLLM, json_schema_from_model, responses_text_format

from .models import TriageReport
from .tools import TRIAGE_ALLOWED, TRIAGE_TOOL_SPECS, ToolRunner, WRITE_TOOLS

PROMPT_FILE = Path(__file__).resolve().parent / "prompts" / "triage.v1.txt"
PROMPT_VERSION = "triage.v1"

INCIDENT_REFUND_500 = "POST /payments/{id}/refunds returns 500 after capture"
RUNAWAY_INCIDENT = "keep calling tools forever"


def load_triage_instructions(path: Path | None = None) -> str:
    prompt_path = path if path is not None else PROMPT_FILE
    return prompt_path.read_text(encoding="utf-8").strip()


def refund_500_trajectory() -> list[dict[str, object]]:
    """Five LLM turns: four tools, then a typed TriageReport."""
    report = TriageReport(
        incident=INCIDENT_REFUND_500,
        root_cause="RefundService NPE after capture; only captured payments can be refunded.",
        evidence=[
            "GET endpoint spec POST /payments/{id}/refunds",
            "corpus: only captured payments can be refunded",
            "log: NullPointerException in RefundService after capture",
        ],
        recommended_action="Guard RefundService on capture state; publish a runbook page.",
        steps=5,
        approved_write=True,
    )
    return [
        {
            "tools": [
                {
                    "call_id": "call_search_1",
                    "name": "search_docs",
                    "arguments": '{"query":"refund 500"}',
                }
            ]
        },
        {
            "tools": [
                {
                    "call_id": "call_spec_2",
                    "name": "get_endpoint_spec",
                    "arguments": '{"method":"POST","path":"/payments/{id}/refunds"}',
                }
            ]
        },
        {
            "tools": [
                {
                    "call_id": "call_corpus_3",
                    "name": "search_corpus",
                    "arguments": '{"query":"refund captured payment"}',
                }
            ]
        },
        {
            "tools": [
                {
                    "call_id": "call_propose_4",
                    "name": "propose_page",
                    "arguments": json.dumps(
                        {
                            "slug": "refund-500",
                            "title": "Refund 500 after capture",
                            "body": "Check capture state before refund.",
                        }
                    ),
                }
            ]
        },
        {"message": report.model_dump_json()},
    ]


def runaway_trajectory(*, rounds: int = 20) -> list[dict[str, object]]:
    turns: list[dict[str, object]] = []
    for index in range(rounds):
        turns.append(
            {
                "tools": [
                    {
                        "call_id": f"call_runaway_{index + 1}",
                        "name": "search_docs",
                        "arguments": '{"query":"ping"}',
                    }
                ]
            }
        )
    return turns


def scripted_triage_llm() -> FakeLLM:
    return FakeLLM(
        trajectories={
            INCIDENT_REFUND_500: refund_500_trajectory(),
            RUNAWAY_INCIDENT: runaway_trajectory(),
        }
    )


def parse_triage_report(text: str, *, steps: int, approved_write: bool) -> TriageReport | None:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict):
        return None
    payload.setdefault("steps", steps)
    payload.setdefault("approved_write", approved_write)
    try:
        return TriageReport.model_validate(payload)
    except ValidationError:
        return None


class TriageDesk:
    """Investigate an incident with the from-scratch agent loop."""

    def __init__(
        self,
        client: FakeLLM | None = None,
        *,
        runner: ToolRunner | None = None,
        max_steps: int = 8,
        approved: bool = False,
    ) -> None:
        self._client = client if client is not None else scripted_triage_llm()
        self._owns_runner = runner is None
        self._runner = (
            runner if runner is not None else ToolRunner(allow=TRIAGE_ALLOWED, approved=approved)
        )
        self.max_steps = max_steps
        self.approved = approved
        self.instructions = load_triage_instructions()

    def close(self) -> None:
        if self._owns_runner:
            self._runner.close()

    def __enter__(self) -> TriageDesk:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def investigate(self, incident: str, *, approved: bool | None = None) -> AgentResult:
        gate = self.approved if approved is None else approved
        self._runner.approved = gate
        memory = AgentMemory(budget_tokens=500)
        trace = AgentTrace(request_id="triage_fake")
        text_format = responses_text_format(
            "triage_report",
            json_schema_from_model(TriageReport),
        )
        result = run_agent_loop(
            self._client,
            incident,
            execute=self._runner.invoke_handled,
            tools=list(TRIAGE_TOOL_SPECS),
            instructions=self.instructions,
            max_steps=self.max_steps,
            approve=gate,
            write_tools=WRITE_TOOLS,
            memory=memory,
            trace=trace,
            text_format=text_format,
        )
        return result

    def report(self, incident: str, *, approved: bool = True) -> TriageReport:
        result = self.investigate(incident, approved=approved)
        if result.status != "done" or not result.output_text:
            raise RuntimeError(f"triage did not finish: status={result.status}")
        parsed = parse_triage_report(
            result.output_text,
            steps=result.steps,
            approved_write=approved,
        )
        if parsed is None:
            raise RuntimeError("triage final message was not a TriageReport")
        return parsed
