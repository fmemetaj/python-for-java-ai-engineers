# 02 — Java concepts, expressed idiomatically in Python

## Collections: streams vs comprehensions

**Java:** `tickets.stream().filter(Ticket::isHigh).map(Ticket::id).toList()`

**Python:** `[ticket["id"] for ticket in tickets if ticket["priority"] == "high"]`

Python comprehensions are good for simple transformations. For complex conditions, use an ordinary named function or loop instead of nesting everything.

## Data classes vs validation

- A Java `record` and Python `@dataclass` remove routine data-container boilerplate.
- Java Bean Validation and Python **Pydantic** can enforce constraints at boundaries.
- Python type hints such as `id: int` help tooling but, by themselves, do **not** reject wrong values at runtime.
- Python `None` is runtime null; `str | None` is a type annotation, not a runtime wrapper like `Optional<String>`.

## Protocols, decorators and context managers

- A `Protocol` captures interface-like behavior using *structural typing*.
- A decorator `@tool` can actually wrap/register a function at definition time; unlike a typical Java annotation it is executable Python logic.
- `with open(...) as file` resembles Java `try (var file = ...)` for automatic cleanup.

## Real gotcha: mutable default arguments

Avoid `def add_tag(tag, tags=[]):`. The same list is reused between calls.

Use `def add_tag(tag, tags=None): tags = [] if tags is None else tags`.

## Checkpoint

Explain why `dict.get("missing")` returns `None` but `dict["missing"]` raises `KeyError`.

[Return to guide index](README.md)
