import pytest
from course_kit.loader import load_concept_module

dashboard = load_concept_module("6_04", "dashboard")


def test_total_cost() -> None:
    rows = [{"cost_usd": 0.00004}, {"event": "other"}, {"cost_usd": 0.00001}]
    assert abs(dashboard.total_cost(rows) - 0.00005) < 1e-12
    assert dashboard.total_cost([]) == 0.0


def test_cache_discount() -> None:
    saved = dashboard.cache_discount(1000, 0.40, 0.10)
    assert abs(saved - 0.0003) < 1e-12
    with pytest.raises(ValueError):
        dashboard.cache_discount(-1, 0.40, 0.10)
