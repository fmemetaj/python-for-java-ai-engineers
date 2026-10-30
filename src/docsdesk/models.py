"""JSON DTOs for the mock docs service. Java analogy: Jackson + Bean Validation."""

from __future__ import annotations

from pydantic import BaseModel, Field


class DocPage(BaseModel):
    slug: str = Field(min_length=1)
    title: str = Field(min_length=1)
    body: str = Field(min_length=1)
