"""Replace Java-style getters with a property."""

from __future__ import annotations


class Budget:
    def __init__(self, cents: int) -> None:
        self._cents = cents

    @property
    def cents(self) -> int:
        """Read the stored integer cents."""
        raise NotImplementedError

    @property
    def dollars(self) -> float:
        """Return cents / 100."""
        raise NotImplementedError

    @dollars.setter
    def dollars(self, value: float) -> None:
        """Store dollars as integer cents (round half toward nearest int via round())."""
        raise NotImplementedError
