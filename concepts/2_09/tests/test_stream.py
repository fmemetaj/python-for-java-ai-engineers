from course_kit.loader import load_concept_module

stream = load_concept_module("2_09", "stream")


def test_assemble() -> None:
    text = stream.assemble_text(
        [
            {"type": "response.output_text.delta", "delta": "Be"},
            {"type": "response.output_text.delta", "delta": "arer"},
            {"type": "response.completed", "delta": ""},
        ]
    )
    assert text == "Bearer"


def test_event_names() -> None:
    assert stream.is_responses_event("response.output_text.delta") is True
    assert stream.is_responses_event("response.completed") is True
    assert stream.is_responses_event("chat.completion.chunk") is False
