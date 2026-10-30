"""Money value object via the data model."""

from __future__ import annotations

from collections.abc import Iterator


class Money:
    def __init__(self, cents: int, currency: str = "USD") -> None:
        self.cents = cents
        self.currency = currency

    def __repr__(self) -> str:
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError

    def __iter__(self) -> Iterator[object]:
        """Yield cents, then currency — so `cents, currency = money` works."""
        raise NotImplementedError

    def __add__(self, other: Money) -> Money:
        """Add cents when the currency matches; otherwise ValueError."""
        raise NotImplementedError


class LineBatch:
    def __init__(self, lines: list[str]) -> None:
        self.lines = lines

    def __len__(self) -> int:
        raise NotImplementedError

    def __bool__(self) -> bool:
        """False when there are no lines."""
        raise NotImplementedError
