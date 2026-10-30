from course_kit.loader import load_concept_module

ask = load_concept_module("a_02", "ask")


def test_refund_screenshot() -> None:
    result = ask.ask_refund_stacktrace()
    assert result.fixture_id == "stacktrace-refund-500"
    assert result.request_id
    assert ask.mentions_npe(result.answer) is True
    assert result.items[1]["type"] == "input_image"
