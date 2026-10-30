# 3.1 Structured outputs (JSON Schema from Pydantic)   [Analog: Jackson DTO + Bean Validation] [cost: mock] [~50 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/3_01/tests/test_skip.py` passes.

Official docs: [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs), [Responses](https://platform.openai.com/docs/guides/migrate-to-responses).

## 1. Concept

**Structured Outputs** make the model fill a JSON Schema instead of free prose. You derive the schema from a Pydantic model (Jackson DTO + Bean Validation). Responses puts the schema in `text.format`. Chat Completions puts it in `response_format`. The model may still **refuse**; always validate the payload.

## 2. Java version

```java
public class StructuredDemo {
    record Incident(String service, String severity, String summary) {}
    public static void main(String[] args) {
        Incident dto = new Incident("auth", "high", "token leak");
        if (dto.service().isBlank()) {
            throw new IllegalArgumentException("service");
        }
        System.out.println(dto.severity());
    }
}
```

Jackson would parse JSON into the record; `@NotBlank` / `@Pattern` would reject empty `service` or a made-up severity.

## 3. Python version

```python
class Incident(BaseModel):
    service: str = Field(min_length=1)
    severity: Literal["low", "medium", "high", "critical"]
    summary: str = Field(min_length=1)
    timestamp: str = Field(min_length=1)


schema = Incident.model_json_schema()
# Responses:  text={"format": {"type": "json_schema", "name": "incident", "strict": True, "schema": schema}}
# Chat:       response_format={"type": "json_schema", "json_schema": {"name": "incident", "schema": schema, "strict": True}}
incident = Incident.model_validate_json(response.output_text)
```

| Java | Python |
| --- | --- |
| Jackson DTO + `@Valid` | Pydantic `BaseModel` + `model_validate_json` |
| `ObjectMapper` schema | `model_json_schema()` → `text.format` |
| `MethodArgumentNotValidException` | `ValidationError` or `response.refusal` |
| OpenAPI `application/json` | JSON Schema (`additionalProperties: false` in strict mode) |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| Bean Validation always runs on the controller | Type hints do **not** validate; Pydantic does | Shipping an unparsed `output_text` string |
| One `Content-Type` | Responses `text.format` vs Chat `response_format` | Copy-pasting Chat Completions into `responses.create` |
| Exceptions for bad JSON | The model can **refuse** instead of emitting schema | Treating refusal as a parse bug |
| `FAIL_ON_UNKNOWN_PROPERTIES` | Strict schemas need `additionalProperties: false` | Extra keys silently accepted |
| Assistants “JSON mode” tutorials | Assistants API sunset 2026-08-26 | Calling a dead API |

## 5. Exercise

Extract a typed `Incident` from model JSON: build the schema, both API payload shapes, and `parse_incident`.

```bash
uv run pytest concepts/3_01
```

- Hint 1: `Incident.model_json_schema()` then set `additionalProperties` to false.
- Hint 2: Responses format is flat (`type`, `name`, `strict`, `schema`). Chat nests under `json_schema`.
- Solution: `solutions/schema.py`.

## 6. Check

1. Where does Responses put the schema — `text.format` or `response_format`?
2. Does `severity: str` on a dataclass reject `"orange"` at runtime?
3. What should you do if `response.refusal` is set?
4. Predict: missing `timestamp` → `ValidationError` or a default?

## Setup / troubleshooting

- Graded work uses `LLM_PROVIDER=fake`. Copy `.env.example` → `.env` only for optional live calls. Never commit `.env`.
- Live path: `client.responses.create` / `client.responses.parse` with `text_format=Incident`. Never the Assistants API.
- If pyright complains about `model_json_schema()`, you are on Pydantic 2 (`>=2.10` in this repo).
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** DocsDesk answers as a `TypedAnswer` (answer + citations + confidence), not a paragraph.

**What you learned:** JSON Schema from Pydantic, two API field names, validate even when the vendor promises “always JSON”.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
