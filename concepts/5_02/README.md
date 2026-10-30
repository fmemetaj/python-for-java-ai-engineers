# 5.2 Agent loop, max steps, stop conditions   [Analog: Spring StateMachine] [cost: mock] [~60 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/5_02/tests/test_skip.py` passes.

Official docs: [Function calling](https://platform.openai.com/docs/guides/function-calling). Responses items: `function_call` out, `function_call_output` back by `call_id`. Never Assistants.

## 1. Concept

The **agent loop** is a state machine you run: `llm` → maybe `tool` → maybe `approval` → `done` / `capped` / `denied`. The model proposes transitions (`function_call`). **You** still cap steps and execute tools. Module 3 taught one tool round; this lesson is the same machine with a hard stop and a scripted 5-step trajectory.

## 2. Java version

```java
public class AgentLoopDemo {
    enum State { START, TOOL, DONE }
    public static State next(State state, boolean hasToolCall) {
        if (state == State.DONE) return State.DONE;
        return hasToolCall ? State.TOOL : State.DONE;
    }
    public static void main(String[] args) {
        System.out.println(next(State.START, true));
    }
}
```

In Spring StateMachine you would declare states and events. The difference: you wrote `next()`. In an LLM agent, `hasToolCall` comes from the model's output items.

## 3. Python version

```python
result = run_agent_loop(
    client,
    incident,
    execute=runner.invoke_handled,
    tools=TRIAGE_TOOL_SPECS,
    max_steps=8,
    approve=True,
)
# result.status in {"done", "capped", "denied"}; result.steps is the complete() count
```

| Java | Python |
| --- | --- |
| `enum State` | `AgentState.status` |
| `sendEvent(TOOL)` | model returns `function_call` |
| `maxRetries` on a listener | `max_steps` on the loop |
| command handler | `ToolRunner.invoke_handled` |
| `@PreAuthorize` | approval gate before `propose_page` |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| Exhaustive `switch` on events | Next event is model-chosen | No `default` → unbounded tool ping-pong without a cap |
| One request / one response | Several `complete()` calls | Forgetting `previous_response_id` / `call_id` (Module 3) |
| Transaction timeout | `max_steps` is *your* control | "The model hung" is usually a missing cap |
| Listener always runs | Write tools need approval | `propose_page` executes because "the LLM asked" |
| Compile-time state graph | Scripted FakeLLM trajectory | Tests that assert wording instead of `status` and `steps` |

Stop conditions, in order: no `function_call` → `done`; write tool + no approval → `denied`; `step == max_steps` while tools remain → `capped`.

## 5. Exercise

Implement `next_status`, `should_stop`, and `run_capped_loop` over a fake `complete()` callable.

```bash
uv run pytest concepts/5_02
```

- Hint 1: each `complete()` is one step. Cap *before* a 4th call if `max_steps=3` and you are still seeing tools.
- Hint 2: `denied` happens when the name is in `write_tools` and `approved` is false — do not execute.
- Solution: `solutions/loop.py`.

## 6. Check

1. Who proposes the next tool — your `switch` or the model?
2. Predict: 4 tool turns + 1 final message, `max_steps=8` — `status` and `steps`?
3. Predict: the same script with `max_steps=3` — `status`?
4. Why is a step cap an engineering control, not a model parameter?

## Setup / troubleshooting

- Scripted FakeLLM `trajectories=` advances one turn per `complete()`. If the second turn still looks like the first, you reused a new FakeLLM instead of the same instance.
- `LLM_PROVIDER=fake` in CI. Live loops bill every round's input tokens.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** DocsDesk `TriageDesk.investigate` replays a 5-step refund-500 trajectory deterministically.

**What you learned:** the loop is a state machine; the model picks transitions; you enforce the cap and the gate.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
