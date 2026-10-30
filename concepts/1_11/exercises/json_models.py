"""Parse docs-service JSON into a Pydantic model."""

from __future__ import annotations

from pydantic import BaseModel, Field


class DocPage(BaseModel):
    slug: str = Field(min_length=1)
    title: str = Field(min_length=1)
    body: str = Field(min_length=1)


def parse_doc(payload: dict[str, object]) -> DocPage:
    """Validate payload as DocPage."""
    raise NotImplementedError


def dump_doc(page: DocPage) -> dict[str, object]:
    """Return a JSON-ready dict (model_dump)."""
    raise NotImplementedError
