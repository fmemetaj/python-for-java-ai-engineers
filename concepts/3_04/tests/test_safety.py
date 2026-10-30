import pytest
from course_kit.loader import load_concept_module

safety = load_concept_module("3_04", "safety")

ALLOW = frozenset({"search_docs", "get_endpoint_spec"})
WRITE = frozenset({"delete_page"})


def test_allow_list() -> None:
    assert safety.is_allowed("search_docs", ALLOW) is True
    assert safety.is_allowed("delete_page", ALLOW) is False
    assert safety.is_allowed("shell", ALLOW) is False


def test_invalid_args_raise() -> None:
    with pytest.raises(ValueError):
        safety.validate_search_args({"query": 1})
    with pytest.raises(ValueError):
        safety.validate_search_args({"query": ""})
    assert safety.validate_search_args({"query": "auth"}) == "auth"


def test_approval_gate() -> None:
    assert safety.run_if_approved("search_docs", write_tools=WRITE, approved=False) is True
    assert safety.run_if_approved("delete_page", write_tools=WRITE, approved=False) is False
    assert safety.run_if_approved("delete_page", write_tools=WRITE, approved=True) is True


def test_idempotency_does_not_rerun() -> None:
    cache: dict[str, str] = {}
    calls = {"n": 0}

    def fn() -> str:
        calls["n"] += 1
        return "ok"

    assert safety.call_once(cache, "k1", fn) == "ok"
    assert safety.call_once(cache, "k1", fn) == "ok"
    assert calls["n"] == 1
    assert safety.call_once(cache, "k2", fn) == "ok"
    assert calls["n"] == 2
