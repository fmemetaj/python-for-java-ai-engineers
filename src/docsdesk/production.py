"""DocsDesk v0.6 production path: measured, observable, budgeted, gated.

Ask() is still FakeLLM in CI. Per-request cost is a structured log field.
Prompt injection is blocked before the model runs. Cache hits skip the LLM.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from course_kit.cost import format_cost

from .assistant import DocsDesk
from .budget import DEFAULT_MODEL, Budget, BudgetExceededError, CostLedger, cost_of, route_model
from .cache import TtlCache
from .observe import bind_from_response, bind_request_id, format_json_log, start_span
from .security import classify_prompt, redact_secrets
from .settings import Settings


@dataclass
class ProductionResult:
    answer: str
    request_id: str
    cost_usd: float
    cached: bool
    model: str
    blocked: bool = False
    log_line: str = ""

    def summary(self) -> str:
        state = "blocked" if self.blocked else ("cache" if self.cached else "live")
        return (
            f"[{state} request_id={self.request_id} model={self.model} "
            f"{format_cost(self.cost_usd)}]"
        )


@dataclass
class ProductionDesk:
    """Wraps DocsDesk with cache, budget, JSON logs, and injection checks."""

    settings: Settings = field(default_factory=Settings.offline)
    desk: DocsDesk | None = None
    budget: Budget | None = None
    cache: TtlCache | None = None
    ledger: CostLedger | None = None
    secrets: tuple[str, ...] = ()
    ttl_seconds: float = 30.0

    def __post_init__(self) -> None:
        if self.desk is None:
            self.desk = DocsDesk()
        if self.budget is None:
            self.budget = Budget(limit_usd=1.0, model=self.settings.openai_model)
        if self.cache is None:
            self.cache = TtlCache()
        if self.ledger is None:
            self.ledger = CostLedger()

    def close(self) -> None:
        if self.desk is not None:
            self.desk.close()

    def __enter__(self) -> ProductionDesk:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def ask(self, question: str) -> ProductionResult:
        if not question.strip():
            raise ValueError("question must be non-empty")
        assert self.desk is not None
        assert self.budget is not None
        assert self.cache is not None
        assert self.ledger is not None
        with start_span("docsdesk.ask", question_len=len(question)):
            if classify_prompt(question) == "injection":
                return self._blocked()
            cached = self.cache.get(question)
            if isinstance(cached, ProductionResult):
                return self._from_cache(cached)
            estimated = 0.0001
            model = route_model(self.budget.remaining_usd, estimated_usd=estimated)
            typed = self.desk.ask(question)
            response = self.desk.last_response
            if response is None:
                raise RuntimeError("DocsDesk did not store last_response")
            request_id = bind_from_response(response, fallback="req_local")
            amount = cost_of(response.usage, model)
            if amount > self.budget.remaining_usd:
                raise BudgetExceededError("call cost exceeds remaining budget")
            self.budget.debit(amount)
            answer = redact_secrets(typed.answer, self.secrets)
            result = ProductionResult(
                answer=answer,
                request_id=request_id,
                cost_usd=amount,
                cached=False,
                model=model,
            )
            self.cache.set(question, result, self.ttl_seconds)
            result.log_line = format_json_log(
                "docsdesk.ask",
                cost_usd=amount,
                cached=False,
                blocked=False,
                model=model,
            )
            self.ledger.record(result.log_line)
            return result

    def _blocked(self) -> ProductionResult:
        assert self.budget is not None
        assert self.ledger is not None
        request_id = bind_request_id("req_blocked")
        model = self.budget.model or DEFAULT_MODEL
        line = format_json_log(
            "docsdesk.ask",
            cost_usd=0.0,
            cached=False,
            blocked=True,
            model=model,
        )
        self.ledger.record(line)
        return ProductionResult(
            answer="blocked: prompt classified as injection",
            request_id=request_id,
            cost_usd=0.0,
            cached=False,
            model=model,
            blocked=True,
            log_line=line,
        )

    def _from_cache(self, cached: ProductionResult) -> ProductionResult:
        assert self.ledger is not None
        request_id = bind_request_id(cached.request_id)
        line = format_json_log(
            "docsdesk.ask",
            cost_usd=0.0,
            cached=True,
            blocked=False,
            model=cached.model,
        )
        self.ledger.record(line)
        return ProductionResult(
            answer=cached.answer,
            request_id=request_id,
            cost_usd=0.0,
            cached=True,
            model=cached.model,
            log_line=line,
        )


__all__ = ["ProductionDesk", "ProductionResult"]
