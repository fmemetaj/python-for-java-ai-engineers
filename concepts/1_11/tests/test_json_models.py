from course_kit.loader import load_concept_module
from pydantic import ValidationError
import pytest

json_models = load_concept_module("1_11", "json_models")


def test_parse_doc() -> None:
    page = json_models.parse_doc(
        {"slug": "auth", "title": "Authentication", "body": "Bearer token"}
    )
    assert page.slug == "auth"
    assert page.title == "Authentication"


def test_empty_body_rejected() -> None:
    with pytest.raises(ValidationError):
        json_models.parse_doc({"slug": "auth", "title": "Authentication", "body": ""})


def test_dump_doc() -> None:
    page = json_models.parse_doc(
        {"slug": "tickets", "title": "Tickets API", "body": "GET /tickets/{id}"}
    )
    dumped = json_models.dump_doc(page)
    assert dumped["slug"] == "tickets"
    assert dumped["body"].startswith("GET")
