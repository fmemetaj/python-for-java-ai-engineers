from course_kit.loader import load_concept_module

logging_util = load_concept_module("1_06", "logging_util")


def test_logger_name() -> None:
    assert logging_util.logger_name("docsdesk.client") == "docsdesk.client"


def test_redact_key() -> None:
    secret = "course-test-secret-value"
    text = logging_util.redact(f"Authorization Bearer {secret}", [secret])
    assert secret not in text
    assert "***" in text


def test_empty_secret_ignored() -> None:
    assert logging_util.redact("hello", [""]) == "hello"
