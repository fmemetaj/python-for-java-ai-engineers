import pytest
from course_kit.loader import load_concept_module

briefs = load_concept_module("7_01", "briefs")


def test_list_briefs() -> None:
    names = briefs.list_briefs()
    assert names == ["own-repo", "pr-review", "log-triage"]


def test_choose_brief() -> None:
    own = briefs.choose_brief("own-repo")
    assert own["id"] == "own-repo"
    assert own["write_tools"] is False
    assert "Java" in own["corpus"]
    review = briefs.choose_brief("PR-review")
    assert review["write_tools"] is True
    triage = briefs.choose_brief("log-triage")
    assert "log" in triage["corpus"].lower()


def test_unknown_brief() -> None:
    with pytest.raises(KeyError):
        briefs.choose_brief("secret-saas")
