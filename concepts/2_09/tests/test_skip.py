from course_kit.loader import load_concept_module

skip = load_concept_module("2_09", "skip")


def test_true_fact() -> None:
    assert skip.responses_stream_uses_typed_events() is True


def test_false_fact() -> None:
    assert skip.reuse_chat_chunk_handlers_unchanged() is False
