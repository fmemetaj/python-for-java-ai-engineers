from course_kit.loader import load_concept_module

config = load_concept_module("1_07", "config")


def test_default_provider() -> None:
    assert config.default_llm_provider() == "fake"


def test_redact_api_key() -> None:
    assert config.redact_env("OPENAI_API_KEY", "course-test-secret-value") == "***"


def test_keep_provider() -> None:
    assert config.redact_env("LLM_PROVIDER", "fake") == "fake"


def test_never_commit_env() -> None:
    assert ".env" in config.files_never_commit()
