# 3.4 Tool safety: validation, allow-lists, approval   [Analog: Input validation, Spring Security authorization] [cost: mock] [~40 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/3_04/tests/test_skip.py` passes.

Official docs: [Function calling](https://platform.openai.com/docs/guides/function-calling) (you still validate — the model is not a security boundary). Reuses the Module 0B `mini_agent` approval idea.

## 1. Concept

A tool call is **untrusted input**. Treat `name` and `arguments` like a public HTTP body: allow-list the name (Spring Security), validate the payload (Bean Validation), require a human gate for writes, and make side-effecting calls **idempotent**.

## 2. Java version

```java
public class ToolSafetyDemo {
    public static boolean allowed(String name) {
        return "search_docs".equals(name);
    }
    public static void main(String[] args) {
        String name = "delete_all";
        if (!allowed(name)) {
            System.out.println("blocked");
            return;
        }
        System.out.println("run");
    }
}
```

You would also `@Valid` the DTO and check `@PreAuthorize` before a delete.

## 3. Python version

```python
ALLOWED = frozenset({"search_docs", "get_endpoint_spec"})
if name not in ALLOWED:
    raise ToolBlockedError(name)
args = SearchDocsArgs.model_validate(payload, strict=True)  # query=1 fails
if needs_approval(name) and not approved:
    raise ApprovalRequiredError(name)
result = call_once(cache, idempotency_key, lambda: run(args))
```

| Java | Python |
| --- | --- |
| Filter / servlet allow-list | `name in ALLOWED_TOOLS` |
| `@Valid` + `@NotBlank` | Pydantic `strict=True` |
| `@PreAuthorize` | `approved` flag (simulated, like `mini_agent`) |
| Idempotent PUT + key | `call_once(cache, key, fn)` |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| Trusting a signed JWT of *your* users | The model is not a user | `shell` / `delete_page` executed because "the LLM asked" |
| Bean Validation on ints vs strings | Default Pydantic **coerces** `1` → `"1"` | Use `strict=True` in this lesson |
| Approval in a real workflow engine | Course approval is **simulated** | Claiming email was sent (it was not) |
| Non-idempotent POST retried | Loop retries look like new calls | Duplicate writes without an idempotency key |

## 5. Exercise

Implement allow-list, `validate_search_args` (no coercion of ints), write-tool approval, and `call_once`. A scripted fake emits invalid args — your validator must raise.

```bash
uv run pytest concepts/3_04
```

- Hint 1: `isinstance(query, str)` and `query.strip()`.
- Hint 2: write tools proceed only when `approved` is True; cache hits skip `fn`.
- Solution: `solutions/safety.py`.

## 6. Check

1. Is the model a security boundary?
2. Why does DocsDesk use `strict=True` for tool args?
3. Which tools in this module need approval? Which do not?
4. Predict: second `call_once` with the same key — does `fn` run?

## Setup / troubleshooting

- Invalid JSON arguments: catch `json.JSONDecodeError` and return an error payload in the loop (do not crash CI).
- Approval is in-memory. Nothing sends email or deletes a page.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** DocsDesk `ToolRunner.invoke_handled` turns `ValidationError` into JSON so the loop can continue. `tests/test_docsdesk_eval.py` includes invalid-arg cases.

**What you learned:** allow-list + strict validation + approval + idempotency; the model is just a caller.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
