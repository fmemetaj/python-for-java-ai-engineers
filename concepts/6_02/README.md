# 6.2 Observability: logs, spans, request IDs   [Analog: Micrometer/OTel, MDC] [cost: mock] [~45 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/6_02/tests/test_skip.py` passes.

Official docs: [OpenTelemetry traces](https://opentelemetry.io/docs/concepts/signals/traces/), [contextvars](https://docs.python.org/3/library/contextvars.html). OpenAI Python SDK: `response._request_id` ([openai-python](https://github.com/openai/openai-python)). Module 5's `AgentTrace` is the agent-loop tree; this lesson is the **request** correlation you ship.

## 1. Concept

Every DocsDesk call gets a **request id** (the HTTP id from the provider, not `response.id`), a **span** (`docsdesk.ask`), and a **JSON log line** that includes `request_id` and `cost_usd`. That is how you debug "this bill, this user, this span" without grepping print().

## 2. Java version

```java
public class ObserveDemo {
    public static void main(String[] args) {
        String requestId = "req-1";
        System.out.println("MDC requestId=" + requestId);
        System.out.println("span docsdesk.ask start");
        System.out.println("span docsdesk.ask end cost=0.000040");
    }
}
```

In production you would call `MDC.put("requestId", id)` and Micrometer/`Observation` around the handler.

## 3. Python version

```python
from docsdesk.observe import bind_from_response, format_json_log, start_span

bind_from_response(response, fallback="req_local")  # copies response.request_id
with start_span("docsdesk.ask"):
    ...
print(format_json_log("docsdesk.ask", cost_usd=0.00004, cached=False))
```

| Java | Python |
| --- | --- |
| MDC `requestId` | `contextvars.ContextVar` (`bind_request_id`) |
| `response.getId()` (entity) | `LLMResponse.id` (`resp_fake_0001`) |
| inbound HTTP request id | `LLMResponse.request_id` (`req_fake_0001`, SDK `_request_id`) |
| Micrometer Timer / OTel span | `start_span` (in-process; no collector) |
| JSON encoder + Logback | `format_json_log` one object per line |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| ThreadLocal MDC | ContextVar follows the task, not the OS thread | asyncio code that copies a thread-local loses the id |
| `response.id` is the request | OpenAI `id` is the **response** object; `_request_id` is the HTTP call | Support tickets quote the wrong identifier |
| DEBUG dump of the SDK object | `_request_id` plus secrets in `repr` | Keys in logs; Module 1's redacting filter still applies |
| Export every span to Jaeger from CI | This course's tracer is in-process | CI hanging on a collector you did not start |

## 5. Exercise

Pick the request id (SDK wins), format a JSON log line, and compute span duration.

```bash
uv run pytest concepts/6_02
```

- Hint 1: empty `sdk_id` → `fallback` (or `req_local`).
- Hint 2: `json.dumps(..., sort_keys=True)` so tests can parse a stable object.
- Solution: `solutions/observe.py`.

## 6. Check

1. Is `resp_fake_0001` the HTTP request id?
2. Why does DocsDesk copy `_request_id` onto a public field?
3. Predict: two asyncio tasks, one ContextVar — do they share the id?
4. Where does per-request **cost** belong — a print, or a log field?

## Setup / troubleshooting

- JSON logs on Windows `cmd.exe` can garble Unicode. Use Windows Terminal; CI sets `PYTHONUTF8=1`.
- `pytest` `caplog` attaches its own handler. DocsDesk tests collect `ledger.lines` instead.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** ProductionDesk writes `{"cost_usd":...,"request_id":"req_fake_0001",...}` on every ask. `tests/test_docsdesk_prod.py` asserts the secret never appears.

**What you learned:** MDC analog is a ContextVar; log `request_id` + `cost_usd`; do not confuse response id with HTTP request id.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
