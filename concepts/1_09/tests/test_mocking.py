from course_kit.loader import load_concept_module

mocking = load_concept_module("1_09", "mocking")


def test_lookup_path() -> None:
    assert mocking.lookup_path("docsdesk.client", "httpx") == "docsdesk.client.httpx"


def test_fetch_title_with_fake_get() -> None:
    def fake_get(url: str) -> dict[str, str]:
        assert url == "/pages/auth"
        return {"title": "Authentication", "slug": "auth"}

    assert mocking.fetch_title(fake_get, "/pages/auth") == "Authentication"
