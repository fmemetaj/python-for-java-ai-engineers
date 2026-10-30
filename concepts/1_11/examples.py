"""Pydantic validates at the JSON boundary; dataclasses do not."""

from __future__ import annotations

from pydantic import BaseModel, Field, ValidationError


class DocPage(BaseModel):
    slug: str = Field(min_length=1)
    title: str
    body: str = Field(min_length=1)


page = DocPage.model_validate({"slug": "auth", "title": "Authentication", "body": "Bearer token"})
assert page.slug == "auth"
try:
    DocPage.model_validate({"slug": "", "title": "x", "body": "y"})
    raise SystemExit("expected ValidationError")
except ValidationError:
    pass
print("1.11 examples ok")
