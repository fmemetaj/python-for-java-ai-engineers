# 5.1 Workflow vs agent decision   [NEW — no Java equivalent] [cost: mock] [~35 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/5_01/tests/test_skip.py` passes. **Still recommended.**

Official docs: [Function calling](https://platform.openai.com/docs/guides/function-calling) (the loop where the *model* picks tools). DocsDesk RAG in Module 4 is the workflow you already built.

## 1. Concept

A **workflow** is a path *you* wrote: retrieve, then answer. An **agent** is a loop where the *model* may call tools zero-to-N times based on what it just observed. A **single call** is one prompt in, one message out. Most "agent" demos are workflows with extra adjectives.

## 2. Intuition

Think of a runbook vs a junior on-call.

```
Workflow (you own the arrows)
  classify → retrieve → answer
Agent (the model owns the next arrow)
  observe? → pick a tool → observe? → pick another? → stop
```

If you can draw the arrows before the request arrives, it is a workflow. If the next tool depends on the previous tool's JSON, it is an agent.

## 3. Why it exists

Fixed pipelines are cheaper, easier to test, and fail in ways you can name. Agents exist for *investigations*: "this 500, find out why" — you do not know whether that means search_docs, get_endpoint_spec, or both, or a write that needs a human. Java would encode the known graph as `enum Step` plus a `switch`. That is the right tool when the graph is known. It is the wrong tool when the model must choose.

### The Java analogy that misleads you

Spring StateMachine / a `Strategy` bean looks like "flexible control flow". You still wrote every transition. An LLM agent is not a Strategy you registered: the next state is a `function_call` item you did not enumerate at compile time. Treating "we have a state machine" as "we have an agent" is how teams wrap a two-step RAG pipeline in a 20-step loop and then wonder why the bill moved.

## 4. Step-by-step examples

**Example 1 — single call.** `classify_ticket(text) → category`. One complete(), no tools. Not an agent.

**Example 2 — workflow.** Module 4 RAG: *you* retrieve k chunks, *you* assemble context, *you* call the model once. The model never chooses `search_corpus`.

**Example 3 — agent.** DocsDesk triage: the model may call `search_docs`, then `get_endpoint_spec`, then `propose_page`. You did not hard-code that order in a `switch`.

**Example 4 — do not wrap a workflow.** Putting "retrieve then answer" inside an agent loop wastes a step cap and tool-round tokens. Use the RAG pipeline.

**Example 5 — the decision rule.** `model_picks_tools and branching and not steps_known` → agent. Anything else → workflow or a single call.

```bash
uv run python concepts/5_01/examples.py
```

The fake cannot teach a live model that takes a surprising branch. Graded tests check *your* classifier, not wording.

## 5. Common pitfalls

- Calling any tool-using program an agent (Module 3's loop is the mechanism; this lesson is *when* to use it).
- Using an agent because a blog post said "agentic".
- Skipping a step cap "because the workflow is short".
- Forgetting that every tool round still bills input tokens (Module 2).

## 6. Exercises

1. **Guided:** `classify_orchestration` and `should_use_agent`.
2. **Open:** `reasons_not_to_use_agent` — return the engineering reasons that apply.

```bash
uv run pytest concepts/5_01
```

- Hint 1: if `model_picks_tools` is false, it cannot be an agent.
- Hint 2: a known, ordered path is a workflow even if an LLM sits in one box.
- Solution: `solutions/decide.py`, `solutions/guide.py`.

## 7. Check

1. Who draws the arrows in a workflow — you or the model?
2. Is DocsDesk RAG (Module 4) a workflow or an agent?
3. Predict: `steps_known=True, model_picks_tools=False` — which label?
4. Why is Spring StateMachine a misleading analog here?
5. Name one cost of wrapping a two-step pipeline in an agent loop.

## Setup / troubleshooting

- Graded work is `LLM_PROVIDER=fake`. This lesson does not call a network.
- If you are unsure, run example 5 and look at the returned label.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** DocsDesk grows a *triage mode* (Module 5) next to the RAG *workflow* (Module 4). Same product, different control flow.

**What you learned:** use an agent only when the model must choose tools on a branching path you could not draw in advance.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
