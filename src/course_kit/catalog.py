"""Module 0A concept index (curriculum.md §6, concepts 0.1–0.15)."""

from __future__ import annotations

from typing import Literal, TypedDict


class Concept(TypedDict):
    id: str
    number: str
    title: str
    kind: Literal["analog", "new"]
    minutes: int
    cost: Literal["mock"]
    java_analog: str
    folder: str


CONCEPTS_0A: tuple[Concept, ...] = (
    {
        "id": "0.1",
        "number": "0.1",
        "title": "Running Python: interpreter, REPL, scripts, if __name__",
        "kind": "analog",
        "minutes": 20,
        "cost": "mock",
        "java_analog": "javac + public static void main, JShell",
        "folder": "0_01",
    },
    {
        "id": "0.2",
        "number": "0.2",
        "title": "Notebooks (Jupyter) — cells, kernel, execution order",
        "kind": "new",
        "minutes": 25,
        "cost": "mock",
        "java_analog": "none",
        "folder": "0_02",
    },
    {
        "id": "0.3",
        "number": "0.3",
        "title": "Variables: names bound to objects, dynamic typing",
        "kind": "analog",
        "minutes": 30,
        "cost": "mock",
        "java_analog": "Typed local variables / var",
        "folder": "0_03",
    },
    {
        "id": "0.4",
        "number": "0.4",
        "title": "Built-in types: int, float, str, bool, None",
        "kind": "analog",
        "minutes": 30,
        "cost": "mock",
        "java_analog": "Primitives + wrappers, String, null",
        "folder": "0_04",
    },
    {
        "id": "0.5",
        "number": "0.5",
        "title": "Truthiness and falsy values",
        "kind": "new",
        "minutes": 20,
        "cost": "mock",
        "java_analog": "none",
        "folder": "0_05",
    },
    {
        "id": "0.6",
        "number": "0.6",
        "title": "Control flow: if/elif, for-in, while, match",
        "kind": "analog",
        "minutes": 30,
        "cost": "mock",
        "java_analog": "if, enhanced for, while, switch patterns",
        "folder": "0_06",
    },
    {
        "id": "0.7",
        "number": "0.7",
        "title": "Functions: def, defaults, keyword args",
        "kind": "analog",
        "minutes": 35,
        "cost": "mock",
        "java_analog": "Methods, overloading, builders",
        "folder": "0_07",
    },
    {
        "id": "0.8",
        "number": "0.8",
        "title": "*args / **kwargs, argument unpacking",
        "kind": "new",
        "minutes": 35,
        "cost": "mock",
        "java_analog": "none (varargs is only a partial analog)",
        "folder": "0_08",
    },
    {
        "id": "0.9",
        "number": "0.9",
        "title": "Scope (LEGB), closures, nonlocal",
        "kind": "new",
        "minutes": 25,
        "cost": "mock",
        "java_analog": "none",
        "folder": "0_09",
    },
    {
        "id": "0.10",
        "number": "0.10",
        "title": "First-class functions and lambdas",
        "kind": "analog",
        "minutes": 25,
        "cost": "mock",
        "java_analog": "Functional interfaces, lambdas, method refs",
        "folder": "0_10",
    },
    {
        "id": "0.11",
        "number": "0.11",
        "title": "Collections: list, dict, set, tuple",
        "kind": "analog",
        "minutes": 40,
        "cost": "mock",
        "java_analog": "ArrayList, HashMap, HashSet, immutable List/record",
        "folder": "0_11",
    },
    {
        "id": "0.12",
        "number": "0.12",
        "title": "Slicing and unpacking",
        "kind": "new",
        "minutes": 25,
        "cost": "mock",
        "java_analog": "none",
        "folder": "0_12",
    },
    {
        "id": "0.13",
        "number": "0.13",
        "title": "List/dict/set comprehensions",
        "kind": "new",
        "minutes": 45,
        "cost": "mock",
        "java_analog": "none",
        "folder": "0_13",
    },
    {
        "id": "0.14",
        "number": "0.14",
        "title": "Iterators, generators and yield",
        "kind": "new",
        "minutes": 50,
        "cost": "mock",
        "java_analog": "none (Iterator<T> is a partial analog)",
        "folder": "0_14",
    },
    {
        "id": "0.15",
        "number": "0.15",
        "title": "Streams vs comprehensions/generators/itertools",
        "kind": "analog",
        "minutes": 25,
        "cost": "mock",
        "java_analog": "Stream API (map/filter/collect)",
        "folder": "0_15",
    },
)

MODULE_0A = {
    "id": "m0a",
    "title": "Python Fundamentals I — core language",
    "cost": "mock",
    "concepts": CONCEPTS_0A,
}
