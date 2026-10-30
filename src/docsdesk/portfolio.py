"""Capstone portfolio helpers: briefs, eval/cost/threat reports, README checklist.

These are the artifacts a Java engineer would put in a hiring packet.
Every number comes from FakeLLM / FakeEmbedder fixtures unless the learner
opts into a live key. Live rates are reported with no threshold claimed.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any

from course_kit.cost import load_pricing
from course_kit.loader import repo_root

from .agent_eval import run_agent_eval
from .evals import CaseResult, EvalReport, run_docsdesk_eval
from .gate import eval_gate
from .prod_eval import run_injection_suite, run_m6_eval
from .retrieval_eval import run_retrieval_eval
from .v1 import DocsDeskV1, V1_VERSION

M7_EVAL_FILE = "data/evals/docsdesk_m7.json"
MIN_CAPSTONE_CASES = 30
DEMO_MINUTES = 5

BRIEFS: dict[str, dict[str, Any]] = {
    "own-repo": {
        "id": "own-repo",
        "title": "DocsDesk over your public Java repo",
        "corpus": "A public Java/Spring repository you own (README + Javadoc).",
        "write_tools": False,
        "notes": "Swap the payments-api fixture for your docs. Keep CI on FakeEmbedder.",
    },
    "pr-review": {
        "id": "pr-review",
        "title": "PR-review assistant for a Spring project",
        "corpus": "A fixture pull-request diff plus the payments-api docs.",
        "write_tools": True,
        "notes": "Approval gate before a simulated review comment. No GitHub network in CI.",
    },
    "log-triage": {
        "id": "log-triage",
        "title": "Log-triage assistant",
        "corpus": "Fixture log lines + endpoint specs + the payments-api corpus.",
        "write_tools": True,
        "notes": "Parse an Incident, then the Module 5 loop. propose_page is simulated.",
    },
}

ARCHITECTURE_LAYERS: tuple[str, ...] = (
    "http",
    "security",
    "budget",
    "rag",
    "agent",
    "observe",
    "evals",
)

README_SECTIONS: tuple[str, ...] = (
    "objective",
    "architecture",
    "how to run",
    "eval report",
    "cost report",
    "threat model",
    "limitations",
    "demo",
)

REQUIRED_ARTIFACTS: tuple[str, ...] = (
    "README",
    "architecture",
    "eval report",
    "cost report",
    "threat model",
    "demo",
)

THREAT_ROWS: tuple[dict[str, str], ...] = (
    {
        "id": "prompt-injection",
        "title": "Prompt injection (direct and indirect)",
        "mitigation": "Classify the user text; strip instruction-like lines from retrieved docs.",
        "residual": "A novel phrasing can still slip past the fixture detectors.",
    },
    {
        "id": "data-leakage",
        "title": "Secrets in answers or logs",
        "mitigation": "Redact known secrets; never log OPENAI_API_KEY (Module 1 filter).",
        "residual": "Unknown secrets are not redacted.",
    },
    {
        "id": "excessive-agency",
        "title": "Write tools without a human",
        "mitigation": "Allow-list tools; propose_page requires an approval flag.",
        "residual": "A buggy approve=True default would skip the gate.",
    },
    {
        "id": "cost-runaway",
        "title": "Unbounded token spend",
        "mitigation": "Per-desk Budget; step cap on the agent loop; FakeLLM in CI.",
        "residual": "A live key with no budget is an invoice, not a test failure.",
    },
    {
        "id": "supply-chain",
        "title": "Model or index lock-in",
        "mitigation": "Own chunker + numpy index; Responses API only; no Assistants.",
        "residual": "Live embeddings still depend on a vendor's vector space.",
    },
)

KNOWN_LIMITATIONS: tuple[str, ...] = (
    "FakeLLM cannot teach live latency, tokenizer drift, or temperature variance.",
    "FakeEmbedder is a hashing trick; it is not a production embedding model.",
    "The approval gate is a boolean in-process flag, not an IdP.",
    "FastAPI is optional and is tested with an in-process TestClient — no bound port.",
    "deploy/Dockerfile is a sketch; CI does not docker build or deploy.",
    "This course never claims a live pass-rate threshold.",
    "propose_page does not write a wiki page, send email, or open a ticket.",
)


@dataclass
class CostReport:
    requests: int
    model: str
    usd_per_request: float
    usd_per_100: float
    pricing_source: str
    pricing_retrieved: str
    assumptions: list[str] = field(default_factory=list)
    provider: str = "fake"

    def summary(self) -> str:
        return (
            f"cost per {self.requests} requests = ${self.usd_per_100:.6f} "
            f"({self.model}, {self.provider}, retrieved {self.pricing_retrieved})"
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "requests": self.requests,
            "model": self.model,
            "usd_per_request": self.usd_per_request,
            "usd_per_100": self.usd_per_100,
            "pricing_source": self.pricing_source,
            "pricing_retrieved": self.pricing_retrieved,
            "assumptions": list(self.assumptions),
            "provider": self.provider,
        }


def choose_brief(name: str) -> dict[str, Any]:
    key = name.strip().lower()
    if key not in BRIEFS:
        known = ", ".join(sorted(BRIEFS))
        raise KeyError(f"unknown brief {name!r}. Known: {known}")
    return dict(BRIEFS[key])


def required_artifacts() -> list[str]:
    return list(REQUIRED_ARTIFACTS)


def architecture_layers() -> list[str]:
    return list(ARCHITECTURE_LAYERS)


def readme_sections() -> list[str]:
    return list(README_SECTIONS)


def demo_minutes() -> int:
    return DEMO_MINUTES


def threat_rows() -> list[dict[str, str]]:
    return [dict(row) for row in THREAT_ROWS]


def known_limitations() -> list[str]:
    return list(KNOWN_LIMITATIONS)


def self_assessment_items() -> list[str]:
    return [
        "uv sync --locked from a clean clone",
        "LLM_PROVIDER=fake for graded work",
        "RAG answers include citations",
        "Write tools require an approval gate",
        "Agent loop enforces a step cap",
        "Eval report has at least 30 cases",
        "Cost per 100 requests is documented",
        "Threat model and limitations are listed",
        "Optional FastAPI uses TestClient (no Docker in CI)",
        "No secrets committed; Responses API only",
    ]


def meets_capstone_bar(total: int, passed: int, *, min_cases: int = MIN_CAPSTONE_CASES) -> bool:
    """True when the bundle is large enough and every case passed on fake."""
    if min_cases < 1:
        raise ValueError("min_cases must be >= 1")
    if total < 0 or passed < 0:
        raise ValueError("counts must be >= 0")
    if passed > total:
        raise ValueError("passed cannot exceed total")
    return total >= min_cases and passed == total


def load_m7_manifest(path: str | None = None) -> dict[str, Any]:
    target = repo_root() / (path if path is not None else M7_EVAL_FILE)
    payload = json.loads(target.read_text(encoding="utf-8"))
    if int(payload.get("min_cases", 0)) < MIN_CAPSTONE_CASES:
        raise ValueError("capstone eval manifest min_cases must be >= 30")
    return payload


def run_v1_eval(*, provider: str | None = None) -> EvalReport:
    """Union of M3–M6 + injection suites. Graded CI is fake-only."""
    name = (provider or os.environ.get("LLM_PROVIDER") or "fake").strip().lower() or "fake"
    if name != "fake":
        raise RuntimeError(
            "DocsDesk v1.0 evals in this course run with LLM_PROVIDER=fake. "
            "Live OpenAI is optional and is not a claimed threshold."
        )
    results: list[CaseResult] = []
    m3 = run_docsdesk_eval(provider="fake")
    results.extend(_prefix("m3", m3.results))
    retrieval = run_retrieval_eval(provider="fake")
    for case in retrieval.cases:
        ok = retrieval.ok and case.recall_at_k > 0
        detail = f"recall={case.recall_at_k:.2f} grounded={case.grounded:.2f}"
        results.append(CaseResult(f"m4:{case.id}", ok, "retrieval", detail))
    agent = run_agent_eval(provider="fake")
    for item in agent.results:
        results.append(CaseResult(f"m5:{item.id}", item.passed, "agent", item.detail))
    m6 = run_m6_eval(provider="fake")
    results.extend(_prefix("m6", m6.results))
    injection = run_injection_suite()
    results.extend(_prefix("inj", injection.results))
    passed = sum(1 for item in results if item.passed)
    return EvalReport(
        passed=passed,
        failed=len(results) - passed,
        total=len(results),
        results=results,
        provider="fake",
    )


def capstone_gate_ok(report: EvalReport, *, min_cases: int = MIN_CAPSTONE_CASES) -> bool:
    return meets_capstone_bar(report.total, report.passed, min_cases=min_cases) and eval_gate(
        report, min_pass_rate=1.0
    )


def cost_per_n(usd_per_request: float, n: int = 100) -> float:
    if usd_per_request < 0 or n < 0:
        raise ValueError("usd_per_request and n must be >= 0")
    return usd_per_request * n


def cost_report_fields() -> list[str]:
    return [
        "requests",
        "model",
        "usd_per_request",
        "usd_per_100",
        "pricing_source",
        "pricing_retrieved",
        "assumptions",
        "provider",
    ]


def build_cost_report(
    *,
    requests: int = 100,
    question: str = "How do clients authenticate?",
) -> CostReport:
    """Scale one FakeLLM ask to ``requests``. Prices come from data/pricing.yaml."""
    if requests < 1:
        raise ValueError("requests must be >= 1")
    table = load_pricing()
    with DocsDeskV1() as desk:
        result = desk.ask(question)
    per = result.cost_usd
    assumptions = [
        "LLM_PROVIDER=fake (no cache hits in this sample)",
        "Responses API shape only — never Assistants",
        f"model={result.model}",
        "no live embeddings; FakeEmbedder + fixture vectors",
        "nothing is deployed; this is a documented estimate",
    ]
    return CostReport(
        requests=requests,
        model=result.model,
        usd_per_request=per,
        usd_per_100=cost_per_n(per, requests),
        pricing_source=table.source,
        pricing_retrieved=table.retrieved,
        assumptions=assumptions,
        provider="fake",
    )


def print_eval_report(report: EvalReport) -> None:
    print(f"DocsDesk v{V1_VERSION} eval (fake, ≥{MIN_CAPSTONE_CASES} cases)")
    print(report.summary())
    print(f"capstone gate {'pass' if capstone_gate_ok(report) else 'fail'}")
    for item in report.results:
        mark = "pass" if item.passed else "fail"
        print(f"  {item.id}: {mark} [{item.check}] {item.detail}")


def print_cost_report(report: CostReport) -> None:
    print(report.summary())
    for line in report.assumptions:
        print(f"  assumption: {line}")
    print(f"  source: {report.pricing_source} ({report.pricing_retrieved})")


def print_portfolio() -> None:
    print(f"DocsDesk v{V1_VERSION} portfolio checklist")
    print("artifacts: " + ", ".join(required_artifacts()))
    print("layers: " + " → ".join(architecture_layers()))
    print("readme: " + ", ".join(readme_sections()))
    print(f"demo minutes: {demo_minutes()}")
    print("threats: " + ", ".join(row["id"] for row in threat_rows()))
    print("limitations:")
    for item in known_limitations():
        print(f"  - {item}")
    print("self-assessment:")
    for item in self_assessment_items():
        print(f"  [ ] {item}")


def _prefix(prefix: str, results: list[CaseResult]) -> list[CaseResult]:
    return [
        CaseResult(f"{prefix}:{item.id}", item.passed, item.check, item.detail) for item in results
    ]


__all__ = [
    "ARCHITECTURE_LAYERS",
    "BRIEFS",
    "CostReport",
    "DEMO_MINUTES",
    "M7_EVAL_FILE",
    "MIN_CAPSTONE_CASES",
    "README_SECTIONS",
    "REQUIRED_ARTIFACTS",
    "architecture_layers",
    "build_cost_report",
    "capstone_gate_ok",
    "choose_brief",
    "cost_per_n",
    "cost_report_fields",
    "demo_minutes",
    "known_limitations",
    "load_m7_manifest",
    "meets_capstone_bar",
    "print_cost_report",
    "print_eval_report",
    "print_portfolio",
    "readme_sections",
    "required_artifacts",
    "run_v1_eval",
    "self_assessment_items",
    "threat_rows",
]
