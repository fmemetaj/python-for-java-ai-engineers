import pytest
from course_kit.loader import load_concept_module

migrate = load_concept_module("2_07", "migrate")


def test_single_user_message() -> None:
    body = migrate.migrate_chat_body_to_responses(
        {
            "model": "gpt-4.1-mini",
            "messages": [
                {"role": "system", "content": "You are DocsDesk."},
                {"role": "user", "content": "What is auth?"},
            ],
            "response_format": {"type": "text"},
        }
    )
    assert body["input"] == "What is auth?"
    assert body["instructions"] == "You are DocsDesk."
    assert body["store"] is False
    assert "messages" not in body
    assert body["text"] == {"format": {"type": "text"}}


def test_rejects_assistants() -> None:
    with pytest.raises(ValueError, match="sunset"):
        migrate.migrate_chat_body_to_responses(
            {"model": "gpt-4.1-mini", "assistant_id": "asst_x", "messages": []}
        )
