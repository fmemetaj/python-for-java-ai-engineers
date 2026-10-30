# 3.3 The tool-call loop (call_id, outputs)   [NEW — no Java equivalent] [cost: mock] [~40 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/3_03/tests/test_skip.py` passes. **Still recommended.**

Official docs: [Function calling](https://platform.openai.com/docs/guides/function-calling).

## 1. Concept

The **tool-call loop** is a conversation between your app and the model: advertise tools → maybe receive `function_call` items → run your code → send `function_call_output` items keyed by `call_id` → repeat until the model returns a message (or you hit a step cap).

## 2. Intuition

The model is a coworker who can *ask* you to look something up. You are still the process that talks to the database. `call_id` is the sticky note that says "this result belongs to that ask".

```
App --(tools + prompt)--> Model
Model --function_call(call_id=C)--> App
App  --runs search_docs--> fixture docs
App --function_call_output(call_id=C)--> Model
Model --message (TypedAnswer JSON)--> App
```

## 3. Why it exists

A single REST response cannot both "need data" and "already have data". The loop is how the model steers without executing your Python. Java would use an explicit state machine you wrote (`enum Step { FETCH, ANSWER }`). Here the **next state is chosen by the model**, which is the part that has no honest Java analog.

### The Java analogy that misleads you

`switch (command)` / Spring `HandlerMapping` looks like tool dispatch (that was 3.2). It does **not** capture the loop: in Java *you* decide the next command. In this API the model may call zero, one, or several tools, then stop, or call another. Treating it as a single request/response is how people drop `call_id` and wonder why the second turn ignores the tool result.

## 4. Step-by-step examples

**Example 1 — a `function_call` is not the answer.** `output_text` is empty until a `message` item appears.

**Example 2 — you run the tool.** `ToolRunner.invoke_handled` hits the fixture catalog. The fake never opens a socket.

**Example 3 — pair by `call_id`.** The output item must reuse the model's id, not a new UUID.

**Example 4 — second `complete()` with `input_items`.** FakeLLM's `after_tools` script returns the final JSON.

**Example 5 — stop conditions.** No more `function_call` items, or `max_steps` (DocsDesk uses 4). An infinite loop is a bug in *your* cap, not "the model hanging".

```bash
uv run python concepts/3_03/examples.py
```

The fake cannot teach a live model that calls a surprising tool. Graded tests check *your* pairing and loop, not wording.

## 5. Common pitfalls

- Building a new `call_id` on the way back.
- Sending Chat Completions `role: tool` messages into Responses `input`.
- No step cap (a confused model can ping-pong).
- Executing a tool whose name was not in *this* request's `tools` list.
- Forgetting `previous_response_id` / replaying output items (state still bills input tokens — Module 2).

## 6. Exercises

1. **Guided:** `loop_is_done`, `collect_outputs`, `mismatched_call_id`.
2. **Open:** `replay_tool_turn` — two `complete()` calls on a scripted FakeLLM.

```bash
uv run pytest concepts/3_03
```

- Hint 1: done ≡ no item with `type == "function_call"`.
- Hint 2: second `complete(..., input_items=outputs, previous_response_id=first.id)`.
- Solution: `solutions/loop.py`, `solutions/replay.py`.

## 7. Check

1. Who decides whether a second tool call happens?
2. What breaks if `call_id` on the output does not match?
3. Is `output_text` reliable while `function_call` items are present?
4. Why is a `max_steps` cap an engineering control, not a model parameter?

## Setup / troubleshooting

- If the second turn still returns a `function_call`, your FakeLLM `after_tools` key must match the **same prompt string**.
- `LLM_PROVIDER=fake` in CI. Live loops cost extra input tokens each round.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** DocsDesk `run_tool_loop` wraps this for `search_docs` / `get_endpoint_spec`.

**What you learned:** the model owns control flow; you own execution, `call_id`, and the step cap.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
