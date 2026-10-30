"""DocsDesk v1.0 — one product that composes Modules 2–6.

Ask path: injection check → cache → RAG with citations → budget debit →
JSON log (`request_id`, `cost_usd`). Investigate path: the Module 5 agent
loop with a human approval gate for write tools. Graded work is
``LLM_PROVIDER=fake`` plus fixture embeddings. Generation uses
Responses-shaped ``complete()``, never Assistants.

Nothing in this module sends email, posts a GitHub review, or writes a
real wiki page. ``propose_page`` is simulated (``would_write``).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from course_kit.cost import format_cost

from .budget import DEFAULT_MODEL, Budget, BudgetExceededError, CostLedger, cost_of, route_model
from .cache import TtlCache
from .models import RagCitation
from .observe import bind_from_response, bind_request_id, format_json_log, start_span
from .rag import RagDesk
from .security import classify_prompt, redact_secrets
from .settings import Settings
from .triage import INCIDENT_REFUND_500, TriageDesk

V1_VERSION = "1.0"


@dataclass
class V1Result:
    """One DocsDesk v1.0 turn: ask, investigate, or blocked."""

    mode: str
    answer: str
    request_id: str
    cost_usd: float
    cached: bool
    blocked: bool = False
    model: str = DEFAULT_MODEL
    citations: list[RagCitation] = field(default_factory=list)
    steps: int = 0
    approved: bool = False
    tool_names: list[str] = field(default_factory=list)
    status: str = "done"
    log_line: str = ""
    span_names: list[str] = field(default_factory=list)

    def summary(self) -> str:
        state = "blocked" if self.blocked else ("cache" if self.cached else self.mode)
        return (
            f"[v{V1_VERSION} {state} request_id={self.request_id} "
            f"cites={len(self.citations)} {format_cost(self.cost_usd)}]"
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "mode": self.mode,
            "answer": self.answer,
            "request_id": self.request_id,
            "cost_usd": self.cost_usd,
            "cached": self.cached,
            "blocked": self.blocked,
            "model": self.model,
            "citations": [cite.model_dump() for cite in self.citations],
            "steps": self.steps,
            "approved": self.approved,
            "tool_names": list(self.tool_names),
            "status": self.status,
            "version": V1_VERSION,
        }


@dataclass
class DocsDeskV1:
    """Portfolio product: RAG + approval-gated agent + production wrappers."""

    settings: Settings = field(default_factory=Settings.offline)
    rag: RagDesk | None = None
    triage: TriageDesk | None = None
    budget: Budget | None = None
    cache: TtlCache | None = None
    ledger: CostLedger | None = None
    secrets: tuple[str, ...] = ()
    ttl_seconds: float = 30.0
    approved: bool = False

    def __post_init__(self) -> None:
        if self.rag is None:
            self.rag = RagDesk()
        if self.triage is None:
            self.triage = TriageDesk(approved=self.approved)
        if self.budget is None:
            self.budget = Budget(limit_usd=1.0, model=self.settings.openai_model)
        if self.cache is None:
            self.cache = TtlCache()
        if self.ledger is None:
            self.ledger = CostLedger()

    def close(self) -> None:
        if self.triage is not None:
            self.triage.close()

    def __enter__(self) -> DocsDeskV1:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def ask(self, question: str) -> V1Result:
        """Retrieve, cite, log cost. Fake embeddings + FakeLLM in CI."""
        if not question.strip():
            raise ValueError("question must be non-empty")
        assert self.rag is not None
        assert self.budget is not None
        assert self.cache is not None
        assert self.ledger is not None
        span_names = ["docsdesk.v1.ask"]
        with start_span("docsdesk.v1.ask", question_len=len(question)):
            if classify_prompt(question) == "injection":
                return self._blocked("ask")
            cached = self.cache.get(question)
            if isinstance(cached, V1Result):
                return self._from_cache(cached)
            estimated = 0.0001
            model = route_model(self.budget.remaining_usd, estimated_usd=estimated)
            span_names.append("retrieve")
            typed = self.rag.ask(question)
            span_names.append("complete")
            response = self.rag.last_response
            if response is None:
                raise RuntimeError("RagDesk did not store last_response")
            request_id = bind_from_response(response, fallback="req_local")
            amount = cost_of(response.usage, model)
            if amount > self.budget.remaining_usd:
                raise BudgetExceededError("call cost exceeds remaining budget")
            self.budget.debit(amount)
            answer = redact_secrets(typed.answer, self.secrets)
            result = V1Result(
                mode="ask",
                answer=answer,
                request_id=request_id,
                cost_usd=amount,
                cached=False,
                model=model,
                citations=list(typed.citations),
                span_names=span_names,
            )
            self.cache.set(question, result, self.ttl_seconds)
            result.log_line = format_json_log(
                "docsdesk.v1.ask",
                cost_usd=amount,
                cached=False,
                blocked=False,
                model=model,
                citations=len(result.citations),
            )
            self.ledger.record(result.log_line)
            return result

    def investigate(self, incident: str, *, approved: bool | None = None) -> V1Result:
        """Multi-step triage. Write tools stop unless ``approved`` is true."""
        if not incident.strip():
            raise ValueError("incident must be non-empty")
        assert self.triage is not None
        assert self.budget is not None
        assert self.ledger is not None
        if classify_prompt(incident) == "injection":
            return self._blocked("investigate")
        gate = self.approved if approved is None else approved
        span_names = ["docsdesk.v1.investigate"]
        with start_span("docsdesk.v1.investigate", incident_len=len(incident)):
            result = self.triage.investigate(incident, approved=gate)
            response = result.response
            model = self.budget.model or DEFAULT_MODEL
            if response is not None:
                request_id = bind_from_response(response, fallback="req_triage")
                amount = cost_of(response.usage, model)
            else:
                request_id = bind_request_id("req_triage")
                amount = 0.0
            if amount > self.budget.remaining_usd:
                raise BudgetExceededError("call cost exceeds remaining budget")
            self.budget.debit(amount)
            answer = redact_secrets(result.output_text or result.status, self.secrets)
            payload = V1Result(
                mode="investigate",
                answer=answer,
                request_id=request_id,
                cost_usd=amount,
                cached=False,
                model=model,
                steps=result.steps,
                approved=gate,
                tool_names=list(result.tool_names),
                status=result.status,
                span_names=span_names,
            )
            payload.log_line = format_json_log(
                "docsdesk.v1.investigate",
                cost_usd=amount,
                cached=False,
                blocked=False,
                model=model,
                steps=result.steps,
                status=result.status,
            )
            self.ledger.record(payload.log_line)
            return payload

    def demo(self) -> list[V1Result]:
        """Five-minute offline walkthrough. Simulated only — no side effects."""
        ask_result = self.ask("How do I refund a captured payment?")
        triage_result = self.investigate(INCIDENT_REFUND_500, approved=True)
        return [ask_result, triage_result]

    def _blocked(self, mode: str) -> V1Result:
        assert self.budget is not None
        assert self.ledger is not None
        request_id = bind_request_id("req_blocked")
        model = self.budget.model or DEFAULT_MODEL
        event = "docsdesk.v1.ask" if mode == "ask" else "docsdesk.v1.investigate"
        line = format_json_log(
            event,
            cost_usd=0.0,
            cached=False,
            blocked=True,
            model=model,
        )
        self.ledger.record(line)
        return V1Result(
            mode=mode,
            answer="blocked: prompt classified as injection",
            request_id=request_id,
            cost_usd=0.0,
            cached=False,
            blocked=True,
            model=model,
            log_line=line,
            span_names=[event],
            status="blocked",
        )

    def _from_cache(self, cached: V1Result) -> V1Result:
        assert self.ledger is not None
        request_id = bind_request_id(cached.request_id)
        line = format_json_log(
            "docsdesk.v1.ask",
            cost_usd=0.0,
            cached=True,
            blocked=False,
            model=cached.model,
            citations=len(cached.citations),
        )
        self.ledger.record(line)
        return V1Result(
            mode=cached.mode,
            answer=cached.answer,
            request_id=request_id,
            cost_usd=0.0,
            cached=True,
            model=cached.model,
            citations=list(cached.citations),
            log_line=line,
            span_names=["docsdesk.v1.ask", "cache"],
        )


__all__ = ["DocsDeskV1", "V1Result", "V1_VERSION"]
