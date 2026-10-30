from course_kit.loader import load_concept_module

prop = load_concept_module("0_17", "properties")


def test_read_cents_and_dollars() -> None:
    budget = prop.Budget(199)
    assert budget.cents == 199
    assert budget.dollars == 1.99


def test_set_dollars_updates_cents() -> None:
    budget = prop.Budget(0)
    budget.dollars = 2.5
    assert budget.cents == 250
    assert budget.dollars == 2.5


def test_no_getter_method_required() -> None:
    budget = prop.Budget(100)
    assert not hasattr(budget, "getCents")
