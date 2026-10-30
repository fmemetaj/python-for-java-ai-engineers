"""JSON DTOs for the mock docs service and typed LLM answers.

Java analogy: Jackson + Bean Validation. Type hints alone do not validate.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class DocPage(BaseModel):
    slug: str = Field(min_length=1)
    title: str = Field(min_length=1)
    body: str = Field(min_length=1)


class EndpointSpec(BaseModel):
    method: str = Field(min_length=1)
    path: str = Field(min_length=1)
    summary: str = Field(min_length=1)


class Incident(BaseModel):
    """Structured extraction target for log lines (concept 3.1)."""

    service: str = Field(min_length=1)
    severity: Literal["low", "medium", "high", "critical"]
    summary: str = Field(min_length=1)
    timestamp: str = Field(min_length=1)


class Citation(BaseModel):
    slug: str = Field(min_length=1)
    quote: str = Field(min_length=1)


class TypedAnswer(BaseModel):
    """DocsDesk v0.3 answer: text plus citations the model must fill."""

    answer: str = Field(min_length=1)
    citations: list[Citation]
    confidence: float = Field(ge=0, le=1)


class SearchDocsArgs(BaseModel):
    query: str = Field(min_length=1)


class GetEndpointSpecArgs(BaseModel):
    method: str = Field(min_length=1)
    path: str = Field(min_length=1)


class RagCitation(BaseModel):
    """Citation against a retrieved chunk (Module 4)."""

    chunk_id: str = Field(min_length=1)
    path: str = Field(min_length=1)
    quote: str = Field(min_length=1)


class RagAnswer(BaseModel):
    """DocsDesk v0.4 RAG answer: prose plus citations into retrieved chunks."""

    answer: str = Field(min_length=1)
    citations: list[RagCitation]


class SearchCorpusArgs(BaseModel):
    query: str = Field(min_length=1)


class GetRecentErrorsArgs(BaseModel):
    service: str = Field(min_length=1)


class ProposePageArgs(BaseModel):
    slug: str = Field(min_length=1)
    title: str = Field(min_length=1)
    body: str = Field(min_length=1)


class TriageReport(BaseModel):
    """DocsDesk v0.5 triage-mode result: a multi-step investigation."""

    incident: str = Field(min_length=1)
    root_cause: str = Field(min_length=1)
    evidence: list[str]
    recommended_action: str = Field(min_length=1)
    steps: int = Field(ge=1)
    approved_write: bool
