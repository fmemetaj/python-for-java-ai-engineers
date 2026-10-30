# 0.16 Classes and objects   [Analog: classes, constructors, private/public] [cost: mock] [~45 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/0_16/tests/test_skip.py` passes.

Related explainer: [notebook 02](../../notebooks/02_typing_pydantic.ipynb).

## 1. Concept

A Python class is a namespace that produces instances. `__init__` is the constructor. The first parameter of every instance method is the instance itself, conventionally named `self` (Java's implicit `this`). There are **no access modifiers**. A leading underscore is a convention, not a compiler rule.

## 2. Java version

```java
public class ClassesDemo {
    static final class Ticket {
        private final int id;
        Ticket(int id) { this.id = id; }
        int getId() { return id; }
    }
    public static void main(String[] args) {
        System.out.println(new Ticket(7).getId());
    }
}
```

`private` is enforced. Overloaded constructors are extra methods with the same name.

## 3. Python version

```python
class Ticket:
    def __init__(self, ticket_id: int, subject: str) -> None:
        self.ticket_id = ticket_id
        self.subject = subject

    def label(self) -> str:
        return f"#{self.ticket_id} {self.subject}"


Ticket(7, "Login").label()
```

A second `__init__` in the same class **replaces** the first. Optional arguments use defaults, not overloads.

| Java | Python |
| --- | --- |
| `this.id = id` | `self.ticket_id = ticket_id` |
| `new Ticket(7)` | `Ticket(7, "Login")` — no `new` |
| `private` / `public` | `_name` convention; everything is reachable |
| Constructor overloads | One `__init__` + defaults |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| Fields declared on the class | Attributes appear when you assign them | A typo `self.subjct = …` silently creates a new attribute |
| `private final int id` | `_id` is still readable as `ticket._id` | "Nobody will touch this" is a hope, not a lock |
| Overloaded constructors | One `__init__` | A second `__init__` wipes the first |
| Forget `this` | Forget `self` in the parameter list | `TypeError: __init__() takes 2 positional arguments but 3 were given` |
| `static` fields | Class attributes shared by all instances | Mutable class attr `tags: list[str] = []` leaks across tickets |

## 5. Exercise

Implement `Ticket`, `make_ticket`, and `is_private_name` in `exercises/classes.py`.

```bash
uv run pytest concepts/0_16
```

- Hint 1: store `self.ticket_id` and `self.subject` in `__init__`.
- Hint 2: a "private" name starts with `_` but not `__`.
- Solution: `solutions/classes.py`.

## 6. Check

1. You write `class Ticket:` and then two `def __init__`. Which one runs?
2. Can a test still read `ticket._cache`?
3. Why does a method defined as `def label():` fail when you call `ticket.label()`?
4. Where should you put a value that must *not* be shared across instances?

## Setup / troubleshooting (Windows, macOS, Linux)

- Select the project's `.venv` interpreter so the editor shows `self` types. System Python often has no project packages.
- `uv run pytest concepts/0_16` from the **repo root**. Running it from inside `concepts/0_16` will miss `course_kit`.
- More: [docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** a Java-style DocsDesk `Ticket` with getters, setters, and four overloaded constructors — replace with one `__init__` and attributes.

**What you learned:** `__init__` + `self`; `_name` is a convention; no constructor overloads.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
