import pytest
from course_kit.loader import load_concept_module

describe = load_concept_module("a_02", "describe")


def test_description_contains_npe() -> None:
    text = describe.fixture_description("stacktrace-refund-500")
    assert "NullPointerException" in text


def test_unknown_id() -> None:
    with pytest.raises(KeyError):
        describe.fixture_description("not-a-fixture")


def test_prompt_shape() -> None:
    prompt = describe.fake_prompt("stacktrace-refund-500", "Why 500?")
    assert prompt.startswith("[image:stacktrace-refund-500]")
    assert "Why 500?" in prompt
