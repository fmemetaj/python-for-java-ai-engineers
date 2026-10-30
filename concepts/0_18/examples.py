"""Dunder methods hook built-in syntax onto your type."""

from __future__ import annotations


class Money:
    def __init__(self, cents: int, currency: str = "USD") -> None:
        self.cents = cents
        self.currency = currency

    def __repr__(self) -> str:
        return f"Money({self.cents!r}, {self.currency!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self.cents == other.cents and self.currency == other.currency

    def __add__(self, other: Money) -> Money:
        return Money(self.cents + other.cents, self.currency)


assert Money(100) + Money(50) == Money(150)
assert repr(Money(1)) == "Money(1, 'USD')"
print("0.18 examples ok")
