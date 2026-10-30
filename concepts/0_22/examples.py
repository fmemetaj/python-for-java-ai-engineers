"""Protocol is structural; ABC is nominal."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol


class Retriever(Protocol):
    def search(self, query: str) -> list[str]: ...


class Memory:
    def search(self, query: str) -> list[str]:
        return [query]


def top(retriever: Retriever, query: str) -> str:
    return retriever.search(query)[0]


class BaseTool(ABC):
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError


assert top(Memory(), "login") == "login"
print("0.22 examples ok")
