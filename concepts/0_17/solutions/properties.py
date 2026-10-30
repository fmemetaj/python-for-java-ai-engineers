"""Replace Java-style getters with a property (solution)."""

from __future__ import annotations


class Budget:
    def __init__(self, cents: int) -> None:
        self._cents = cents

    @property
    def cents(self) -> int:
        """Read the stored integer cents."""
        return self._cents

    @property
    def dollars(self) -> float:
        """Return cents / 100."""
        return self._cents / 100

    @dollars.setter
    def dollars(self, value: float) -> None:
        """Store dollars as integer cents (round half toward nearest int via round())."""
        self._cents = int(round(value * 100))
