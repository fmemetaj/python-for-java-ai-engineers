import pytest
from course_kit.loader import load_concept_module

perf = load_concept_module("6_03", "perf")


def test_cache_get_hit_and_ttl() -> None:
    store: dict[str, tuple[str, float]] = {}
    calls = {"n": 0}

    def compute() -> str:
        calls["n"] += 1
        return "Bearer"

    value, hit = perf.cache_get(store, "auth", compute, now=0.0, ttl=10.0)
    assert (value, hit, calls["n"]) == ("Bearer", False, 1)
    value, hit = perf.cache_get(store, "auth", compute, now=5.0, ttl=10.0)
    assert (value, hit, calls["n"]) == ("Bearer", True, 1)
    value, hit = perf.cache_get(store, "auth", compute, now=10.0, ttl=10.0)
    assert hit is False
    assert calls["n"] == 2


def test_is_timeout() -> None:
    assert perf.is_timeout(4.9, 5.0) is False
    assert perf.is_timeout(5.0, 5.0) is True
    with pytest.raises(ValueError):
        perf.is_timeout(-1.0, 5.0)


def test_merge_in_order() -> None:
    assert perf.merge_in_order(["a", "b"]) == ["a", "b"]
    assert perf.merge_in_order([]) == []
