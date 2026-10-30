# 5.4 Tracing and debugging agent runs   [Analog: Micrometer / OpenTelemetry] [cost: mock] [~45 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/5_04/tests/test_skip.py` passes.

Official docs: [OpenTelemetry traces](https://opentelemetry.io/docs/concepts/signals/traces/). OpenAI exposes `_request_id` on SDK errors ([Python SDK](https://github.com/openai/openai-python)).

## 1. Concept

An **agent trace** is a tree of spans for one investigate() call: `agent.run` → `llm.step_N` → `tool.search_docs` → `approval.propose_page`. You debug *which step* failed, not a wall of print()s. This course's tracer is in-process and offline. It does not export to Jaeger.

## 2. Java version

```java
public class TraceDemo {
    static final class Span {
        final String name;
        final long durationMs;
        Span(String name, long durationMs) {
            this.name = name;
            this.durationMs = durationMs;
        }
    }
    public static void main(String[] args) {
        System.out.println(new Span("tool.search_docs", 12).name);
    }
}
```

Micrometer/`Observation` and OTel `Tracer.spanBuilder("tool.search_docs")` are the production analog. You already use them around Spring MVC. Put the same around each agent step.

## 3. Python version

```python
trace = AgentTrace(request_id="triage_fake")
with trace.span("tool.search_docs", "tool", call_id="call_1") as span:
    runner.invoke_handled("search_docs", '{"query":"refund"}')
# trace.as_list() → [{name, kind, duration_ms, attributes, children}]
```

| Java | Python |
| --- | --- |
| `Observation.createNotStarted` | `AgentTrace.start_span` |
| `try (var scope = span.makeCurrent())` | `with trace.span(...)` |
| MDC `requestId` | `trace.request_id` |
| span attributes | `span.attributes` |
| Zipkin/Jaeger export | `as_list()` in tests (no collector) |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| Filter logs by `requestId` | You must *set* `request_id` | Two triage runs look like one blob |
| Span per HTTP handler | Span per *LLM step* and *tool* | One span around the whole loop hides the cap |
| Micrometer timers in ms | `time.monotonic()` | `time.time()` jumps; tests should not assert exact ms |
| Export to a collector | In-process list | Graded tests never need Grafana |
| Log the prompt | Redact secrets (Module 1) | API keys in span attributes |

Debugging recipe: print `status`, `steps`, `tool_names`, then the span tree. If `capped`, the last span is still `tool.*`. If `denied`, look for `approval.*`.

## 5. Exercise

Implement `start_span` / `end_span` / `duration_ms` / `as_list` on a tiny `Trace`.

```bash
uv run pytest concepts/5_04
```

- Hint 1: store `start_ms` from a clock callable so tests can inject `lambda: t`.
- Hint 2: children append to the current open span, else to the root list.
- Solution: `solutions/trace.py`.

## 6. Check

1. What is the correlation key across LLM + tool spans?
2. Predict: a 5-step success — how many `llm.step_*` spans?
3. Why not one span around the entire loop?
4. Must CI export to an OTel collector?

## Setup / troubleshooting

- Durations can be 0.0 on a fast fake. Assert `duration_ms >= 0`, not `> 10`.
- Never put `OPENAI_API_KEY` in attributes. Doctor already hides the value.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** `TriageDesk.investigate` returns `result.trace.as_list()` so evals can see tool order.

**What you learned:** treat an agent run like a distributed request — spans, a request id, no secrets.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
