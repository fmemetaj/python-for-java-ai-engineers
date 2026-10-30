"""DocsDesk — a docs HTTP client that grows module by module.

Module 1: settings, redacting logs, httpx + retries, Pydantic JSON, fake LLM.
Module 2: answer from a pasted doc, print tokens and USD, multi-turn session.
Module 3: typed answers with citations, search_docs / get_endpoint_spec, evals.
Module 4: embeddings, in-memory vector search, RAG over a Spring fixture, retrieval evals.
Module 5: triage-mode agent loop, memory, traces, approval gate, agent evals.
Module 6: judge + CI gate, JSON logs / request ids, cache, budgets, injection suite,
optional FastAPI (no bound port in CI).
Module 7: DocsDesk v1.0 capstone — RAG + citations, approval-gated agent,
evals as a CI gate (≥30 cases), tracing, cost budgets, optional FastAPI,
portfolio reports (eval, cost, threat model, README/demo).
Electives (A): optional vision, hosted-vs-own comparison, spend-capped smoke.
Everything essential runs offline (`LLM_PROVIDER=fake`, fixture HTTP transport).
"""

from .agent_eval import AgentEvalReport, run_agent_eval
from .assistant import DocsDesk, default_docsdesk, parse_typed_answer
from .client import DocsClient
from .evals import EvalReport, format_live_rate, run_docsdesk_eval
from .gate import eval_gate
from .prod_eval import run_injection_suite, run_m6_eval
from .portfolio import CostReport, build_cost_report, run_v1_eval
from .production import ProductionDesk, ProductionResult
from .logging_setup import RedactingFilter, configure_logging
from .models import (
    Citation,
    DocPage,
    EndpointSpec,
    Incident,
    RagAnswer,
    RagCitation,
    TriageReport,
    TypedAnswer,
)
from .rag import RagDesk
from .retrieval_eval import RetrievalReport, run_retrieval_eval
from .session import DeskSession, Turn, default_session, load_instructions
from .settings import Settings
from .tools import ToolBlockedError, ToolRunner
from .triage import TriageDesk
from .v1 import DocsDeskV1, V1Result, V1_VERSION
from .vision import VisionAnswer, VisionDesk

__all__ = [
    "AgentEvalReport",
    "Citation",
    "CostReport",
    "DeskSession",
    "DocsDeskV1",
    "DocPage",
    "DocsClient",
    "DocsDesk",
    "EndpointSpec",
    "EvalReport",
    "Incident",
    "ProductionDesk",
    "ProductionResult",
    "RagAnswer",
    "RagCitation",
    "RagDesk",
    "RedactingFilter",
    "RetrievalReport",
    "Settings",
    "ToolBlockedError",
    "ToolRunner",
    "TriageDesk",
    "TriageReport",
    "Turn",
    "TypedAnswer",
    "V1Result",
    "V1_VERSION",
    "VisionAnswer",
    "VisionDesk",
    "build_cost_report",
    "configure_logging",
    "default_docsdesk",
    "default_session",
    "eval_gate",
    "format_live_rate",
    "load_instructions",
    "parse_typed_answer",
    "run_agent_eval",
    "run_docsdesk_eval",
    "run_injection_suite",
    "run_m6_eval",
    "run_retrieval_eval",
    "run_v1_eval",
]
