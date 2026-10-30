"""Spend-capped smoke checklist against FakeLLM. No live key, no Assistants."""

from __future__ import annotations

from dataclasses import dataclass

from course_kit.cost import cost_usd, format_cost, load_pricing
from course_kit.llm import FakeLLM
from course_kit.upgrade import SmokeCall, SmokeReport, run_smoke, sanitize_record

from .settings import Settings

SMOKE_PROMPTS = (
    ("auth", "How do clients authenticate?"),
    ("refund", "How do I refund a captured payment?"),
    ("health", "What is DocsDesk?"),
)


@dataclass(frozen=True)
class ElectiveSmoke:
    report: SmokeReport
    fixture: dict[str, object]

    def summary(self) -> str:
        return (
            f"[smoke ran={len(self.report.ran)} skipped={len(self.report.skipped)} "
            f"spent={format_cost(self.report.spent_usd)} cap={format_cost(self.report.cap_usd)}]"
        )


def plan_smoke_calls(*, cap_usd: float = 0.01, model: str = "gpt-4.1-mini") -> list[SmokeCall]:
    """Price one FakeLLM complete() per prompt, then apply the cap."""
    del cap_usd
    llm = FakeLLM(script={"How do clients authenticate?": "Bearer token"})
    table = load_pricing()
    calls: list[SmokeCall] = []
    for name, prompt in SMOKE_PROMPTS:
        response = llm.complete(prompt)
        amount = cost_usd(response.usage, model, table)
        calls.append(SmokeCall(name=name, cost_usd=amount))
    return calls


def run_elective_smoke(*, cap_usd: float = 0.01) -> ElectiveSmoke:
    settings = Settings.offline()
    if settings.llm_provider != "fake":
        raise RuntimeError("graded smoke tests require LLM_PROVIDER=fake")
    calls = plan_smoke_calls(cap_usd=cap_usd, model=settings.openai_model)
    report = run_smoke(calls, cap_usd)
    raw = {
        "provider": "fake",
        "api": "responses",
        "ran": list(report.ran),
        "skipped": list(report.skipped),
        "spent_usd": report.spent_usd,
        "cap_usd": report.cap_usd,
        "note": "do not paste keys; this fixture is already fake",
    }
    return ElectiveSmoke(report=report, fixture=sanitize_record(raw))
