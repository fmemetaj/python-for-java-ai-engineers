from course_kit.loader import load_concept_module

client = load_concept_module("2_01", "client")


def test_default_is_fake() -> None:
    assert client.resolve_provider(None, {}) == "fake"
    assert client.resolve_provider(None, {"LLM_PROVIDER": ""}) == "fake"


def test_env_provider() -> None:
    assert client.resolve_provider(None, {"LLM_PROVIDER": "openai"}) == "openai"
    assert client.resolve_provider("ollama", {"LLM_PROVIDER": "openai"}) == "ollama"


def test_responses_body_shape() -> None:
    body = client.responses_body("gpt-4.1-mini", "You are DocsDesk.", "What is auth?")
    assert body["input"] == "What is auth?"
    assert body["instructions"] == "You are DocsDesk."
    assert body["store"] is False
    assert "messages" not in body
    assert "assistant_id" not in body


def test_key_not_leaked_when_absent() -> None:
    assert client.key_leaked("provider=fake", "") is False
    assert client.key_leaked("calling course-test-secret-value", "course-test-secret-value") is True
    assert client.key_leaked("calling ***", "course-test-secret-value") is False
