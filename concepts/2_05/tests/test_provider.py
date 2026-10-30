import pytest
from course_kit.loader import load_concept_module

provider = load_concept_module("2_05", "provider")


def test_default() -> None:
    assert provider.resolve_provider(None) == "fake"
    assert provider.resolve_provider(" ") == "fake"


def test_known() -> None:
    assert provider.resolve_provider("OpenAI") == "openai"
    assert provider.is_live("openai") is True
    assert provider.is_live("fake") is False


def test_unknown() -> None:
    with pytest.raises(ValueError, match="Unknown"):
        provider.resolve_provider("assistants")
