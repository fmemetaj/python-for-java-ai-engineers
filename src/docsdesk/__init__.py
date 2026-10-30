"""DocsDesk — a docs HTTP client that grows module by module.

Module 1: settings, redacting logs, httpx + retries, Pydantic JSON, fake LLM.
Module 2: answer from a pasted doc, print tokens and USD, multi-turn session.
Module 3: typed answers with citations, search_docs / get_endpoint_spec, evals.
Module 4: embeddings, in-memory vector search, RAG over a Spring fixture, retrieval evals.
Module 5: triage-mode agent loop, memory, traces, approval gate, agent evals.
Everything essential runs offline (`LLM_PROVIDER=fake`, fixture HTTP transport).
"""

from .agent_eval import AgentEvalReport, run_agent_eval
from .assistant import DocsDesk, default_docsdesk, parse_typed_answer
from .client import DocsClient
from .evals import EvalReport, format_live_rate, run_docsdesk_eval
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

__all__ = [
    "AgentEvalReport",
    "Citation",
    "DeskSession",
    "DocPage",
    "DocsClient",
    "DocsDesk",
    "EndpointSpec",
    "EvalReport",
    "Incident",
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
    "configure_logging",
    "default_docsdesk",
    "default_session",
    "format_live_rate",
    "load_instructions",
    "parse_typed_answer",
    "run_agent_eval",
    "run_docsdesk_eval",
    "run_retrieval_eval",
]
