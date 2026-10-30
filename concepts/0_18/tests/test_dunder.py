import pytest
from course_kit.loader import load_concept_module

dunder = load_concept_module("0_18", "dunder")


def test_money_repr_eq_iter() -> None:
    money = dunder.Money(199, "USD")
    assert repr(money) == "Money(199, 'USD')"
    assert money == dunder.Money(199, "USD")
    assert money != dunder.Money(199, "EUR")
    cents, currency = money
    assert cents == 199
    assert currency == "USD"


def test_money_add() -> None:
    total = dunder.Money(100) + dunder.Money(50)
    assert total == dunder.Money(150, "USD")
    with pytest.raises(ValueError):
        _ = dunder.Money(1, "USD") + dunder.Money(1, "EUR")


def test_line_batch_len_and_bool() -> None:
    empty = dunder.LineBatch([])
    full = dunder.LineBatch(["ERROR disk"])
    assert len(empty) == 0
    assert not empty
    assert len(full) == 1
    assert bool(full) is True
