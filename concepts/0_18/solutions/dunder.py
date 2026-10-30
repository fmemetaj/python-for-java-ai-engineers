"""Money value object via the data model (solution)."""

from __future__ import annotations

from collections.abc import Iterator


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

    def __iter__(self) -> Iterator[object]:
        """Yield cents, then currency — so `cents, currency = money` works."""
        yield self.cents
        yield self.currency

    def __add__(self, other: Money) -> Money:
        """Add cents when the currency matches; otherwise ValueError."""
        if self.currency != other.currency:
            raise ValueError(f"currency mismatch: {self.currency} vs {other.currency}")
        return Money(self.cents + other.cents, self.currency)


class LineBatch:
    def __init__(self, lines: list[str]) -> None:
        self.lines = lines

    def __len__(self) -> int:
        return len(self.lines)

    def __bool__(self) -> bool:
        """False when there are no lines."""
        return len(self.lines) > 0
