from course_kit.loader import load_concept_module

errors = load_concept_module("2_07", "errors")


def test_flags() -> None:
    assert errors.is_migration_error("print(resp.choices[0].message.content)") is True
    assert errors.is_migration_error("previous_response_id is free context") is True
    assert errors.is_migration_error("print(response.output_text)") is False


def test_extract_responses() -> None:
    text = errors.extract_text(
        {
            "object": "response",
            "output": [
                {"type": "reasoning", "summary": []},
                {
                    "type": "message",
                    "content": [{"type": "output_text", "text": "Bearer token"}],
                },
            ],
        }
    )
    assert text == "Bearer token"


def test_extract_chat() -> None:
    text = errors.extract_text(
        {
            "object": "chat.completion",
            "choices": [{"message": {"role": "assistant", "content": "Bearer token"}}],
        }
    )
    assert text == "Bearer token"
