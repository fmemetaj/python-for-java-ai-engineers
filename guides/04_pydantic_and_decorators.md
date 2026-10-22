# 04 — Pydantic, type hints and decorators

A Python annotation `count: int` does not stop a caller from passing a string at runtime. Validate **untrusted input** using Pydantic:

```python
from pydantic import BaseModel, Field

class Ticket(BaseModel):
    id: int = Field(gt=0)
    subject: str = Field(min_length=2)

Ticket(id=1, subject="Help")  # valid
# Ticket(id=-1, subject="x")  # raises ValidationError
```

## Why structured outputs matter in AI apps

LLM responses are probabilistic text. Even when asked to produce JSON, they can be malformed or violate expected values. A Pydantic schema enforces your local contract. **Validation isn't a guarantee that generated factual claims are true.**

The optional Ollama demo validates:

```python
class ModelSuggestion(BaseModel):
    category: Literal["access", "billing", "general"]
    suggested_reply: str = Field(min_length=8)
```

## Decorators

```python
def trace(fn):
    def wrapped(*args, **kwargs):
        print("calling", fn.__name__)
        return fn(*args, **kwargs)
    return wrapped

@trace
def lookup():
    return "result"
```

`@trace` has the effect of `lookup = trace(lookup)`. Agent tool decorators may register a callable's schema and metadata.

**Exercise:** add a `priority` field limited to `low`, `normal`, `high`. Which test rejects `priority="urgent"`?

[Return to guide index](README.md)
