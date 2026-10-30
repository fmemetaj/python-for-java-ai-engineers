"""@property is an attribute with a function behind it."""

from __future__ import annotations


class Budget:
    def __init__(self, cents: int) -> None:
        self._cents = cents

    @property
    def dollars(self) -> float:
        return self._cents / 100


assert Budget(250).dollars == 2.5
print("0.17 examples ok")
