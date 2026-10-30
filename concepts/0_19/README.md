# 0.19 Dataclasses and Pydantic   [Analog: records, Lombok, Jackson DTOs + Bean Validation] [cost: mock] [~35 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/0_19/tests/test_skip.py` passes.

Related explainer: [notebook 02](../../notebooks/02_typing_pydantic.ipynb).

## 1. Concept

`@dataclass` generates `__init__`, `__repr__`, and `__eq__` from annotated fields — like a Java record. It does **not** validate types at runtime. **Pydantic** `BaseModel` does validate, at the process boundary (JSON, HTTP, LLM output). Type hints stay editor/CI guidance (0.23).

## 2. Java version

```java
public class DataclassesDemo {
    record Ticket(int id, String subject) {}
    public static void main(String[] args) {
        var t = new Ticket(1, "Login");
        System.out.println(t.id() + " " + t.subject());
    }
}
```

Jackson + Bean Validation sit in front of the record when the payload is untrusted.

## 3. Python version

```python
@dataclass(frozen=True)
class LogLine:
    level: str
    message: str


class TicketIn(BaseModel):
    id: int = Field(gt=0)
    subject: str = Field(min_length=2)


LogLine("ERROR", "disk")  # no runtime type check
TicketIn.model_validate({"id": 1, "subject": "Login"})
```

`LogLine(1, "disk")` is accepted by the interpreter. `TicketIn(id=0, …)` raises `ValidationError`.

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| Record + javac types | Dataclass stores whatever you pass | `LogLine(1, "x")` is a silent shape bug |
| Bean Validation on the DTO | Pydantic on the **boundary** | Using dataclass for HTTP/LLM input |
| `equals` from the record | Dataclass `__eq__` compares fields | `frozen=True` is needed before hashing |
| Jackson `@JsonIgnore` | `model_dump()` / `Field` options | Dumping secrets into logs (never do that) |

## 5. Exercise

Implement `parse_log_line` (dataclass) and `parse_ticket` (Pydantic `model_validate`) in `exercises/models.py`.

```bash
uv run pytest concepts/0_19
```

- Hint 1: `level, _, message = text.partition(" ")`.
- Hint 2: `return TicketIn.model_validate(data)`.
- Solution: `solutions/models.py`.

## 6. Check

1. Does `@dataclass` raise if `level` is an `int`?
2. Where should Pydantic live — inside a hot loop, or at input/output?
3. Why `frozen=True` on `LogLine`?
4. `TicketIn(id="1", subject="Login")` — Pydantic may coerce. Is that javac behaviour?

## Setup / troubleshooting

- `ModuleNotFoundError: pydantic` → this interpreter is not `.venv`. `uv sync --locked --group dev` then `uv run pytest`.
- Windows: JSON fixtures must be UTF-8. This repo's `.gitattributes` sets `eol=lf`.

**Real scenario:** DocsDesk accepts a ticket JSON blob with Pydantic and keeps parsed log lines as frozen dataclasses.

**What you learned:** dataclass ≈ record (no validation); Pydantic ≈ Bean Validation at the boundary.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
