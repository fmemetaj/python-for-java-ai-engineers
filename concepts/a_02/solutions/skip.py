"""Solutions for the skip check for A.2."""


def fake_vision_reads_catalog_text_not_pixels() -> bool:
    """Does FakeLLM 'see' the fixture description rather than real pixels?"""
    return True


def screenshot_answers_must_cite_the_fixture_id() -> bool:
    """Should a DocsDesk vision answer be tied to a catalog fixture id?"""
    return True
