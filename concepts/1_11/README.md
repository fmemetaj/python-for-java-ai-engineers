# 1.11 JSON ↔ Pydantic   [Analog: Jackson + Bean Validation] [cost: mock] [~30 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/1_11/tests/test_skip.py` passes.

Official docs: [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/). Related: concept 0.19.

## 1. Concept

HTTP JSON is untyped until you validate it. **Pydantic** `BaseModel.model_validate` is Jackson databind plus Bean Validation: parse, coerce, reject. Type hints on a dataclass do **not** do this at runtime.

## 2. Java version

```java
public class JsonDemo {
    record DocPage(String slug, String title, String body) {}
    public static void main(String[] args) {
        var page = new DocPage("auth", "Authentication", "Bearer token");
        System.out.println(page.slug());
    }
}
```

Jackson would fill the record from JSON; `@NotBlank` would reject `""`.

## 3. Python version

```python
class DocPage(BaseModel):
    slug: str = Field(min_length=1)
    title: str = Field(min_length=1)
    body: str = Field(min_length=1)


page = DocPage.model_validate({"slug": "auth", "title": "Authentication", "body": "Bearer"})
page.model_dump()  # back to JSON-ready dict
```

| Java | Python |
| --- | --- |
| Jackson `ObjectMapper.readValue` | `Model.model_validate` / `model_validate_json` |
| `@NotBlank` / `@Size` | `Field(min_length=...)` |
| `writeValueAsString` | `model_dump` / `model_dump_json` |
| record / DTO | `BaseModel` (runtime) vs `@dataclass` (no validation) |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| FAIL_ON_UNKNOWN_PROPERTIES | Pydantic v2 ignores extras by default unless `extra="forbid"` | Silently dropping fields |
| Bean Validation on the controller | Validate at the **boundary**, then pass models inward | Re-validating on every call, or never validating |
| `Optional` vs empty string | `""` is a present `str`; use `min_length` | Empty body becomes a "valid" page |
| Checked `JsonProcessingException` | `ValidationError` is runtime | Forgetting to test the empty-body case |

## 5. Exercise

`parse_doc` / `dump_doc` around `DocPage`. Empty `body` must raise `ValidationError`.

```bash
uv run pytest concepts/1_11
```

- Hint 1: `DocPage.model_validate(payload)`.
- Hint 2: `page.model_dump()`.
- Solution: `solutions/json_models.py`.

## 6. Check

1. Why not `payload["slug"]` and hope?
2. Does `slug: str` on a dataclass reject `slug=1`?
3. Where should DocsDesk validate — in the httpx client, or in every caller?
4. Predict: extra JSON key `author` with default Pydantic config.

## Setup / troubleshooting

- **pyright vs Pydantic:** hints on the model are for the editor; `ValidationError` is the runtime gate.
- **Windows JSON files:** `encoding="utf-8"` when reading fixtures from disk.
- More: [troubleshooting](../../docs/setup/troubleshooting.md).

**Real scenario:** the mock docs service returns `{slug, title, body}`. `DocsClient.get_page` validates into `DocPage` so a missing `body` fails the request, not a later `KeyError` in a prompt.

**What you learned:** Pydantic is Jackson + Bean Validation at the process boundary.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
