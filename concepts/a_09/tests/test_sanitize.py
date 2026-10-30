from course_kit.loader import load_concept_module

sanitize = load_concept_module("a_09", "sanitize")


def test_redacts_nested() -> None:
    payload = {
        "headers": {"Authorization": "Bearer super-secret-token"},
        "body": "key=sk-abcdefghijklmnop and course-test-secret-value",
        "ok": True,
    }
    cleaned = sanitize.sanitize(payload)
    blob = str(cleaned)
    assert "sk-abcdefghijklmnop" not in blob
    assert "super-secret-token" not in blob
    assert "course-test-secret-value" not in blob
    assert "***" in cleaned["headers"]["Authorization"]
    assert cleaned["ok"] is True
