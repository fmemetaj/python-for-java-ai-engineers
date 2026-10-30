# A.5 Fake hosted-tool loop   [NEW — no Java equivalent] [cost: mock] [~50 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/a_05/tests/test_skip.py` passes. **Still recommended.**

Official docs: [Tools](https://platform.openai.com/docs/guides/tools), [file_search](https://platform.openai.com/docs/guides/tools-file-search). Helper: `course_kit.hosted.next_hosted_turn`.

## 1. Concept

A **hosted-tool loop** is the model emitting a `file_search_call` (or `web_search_call`) that *the platform* runs. You do not dispatch it like Module 3 `function_call`. The fake is two steps: tool, then cited message. Step 2 raises.

## 2. Intuition

Module 3: you run the function and send `function_call_output` by `call_id`. Hosted tools: OpenAI runs the search. Your job is to **cap turns** and read citations, not to implement BM25.

```
step 0: file_search_call (fs_1, completed)
step 1: message + citation ids
step 2: stop (ValueError in the fake)
```

## 3. Why it exists

Hosted tools hide the retrieval implementation. That is convenient and untestable. A two-step fake teaches the *shape* without a paid vector store.

### The Java analogy that misleads you

A Spring `@Service` that calls Elasticsearch is still *your* query. Hosted file_search is closer to "the framework ran a query you never wrote". Command-pattern dispatch from Module 3 does not apply.

## 4. Step-by-step examples

**Example 1 — step 0 is a tool call.** `call_id=fs_1`, `type=file_search_call`.

**Example 2 — step 1 is the cited text.** Citations are hosted chunk ids.

**Example 3 — cap.** `next_hosted_turn(2, …)` raises.

**Example 4 — empty hits.** Message text is `No hosted hits.`

**Example 5 — honesty.** No live latency, no vendor chunker, no web.

```bash
uv run python concepts/a_05/examples.py
```

## 5. Common pitfalls

- Dispatching `file_search_call` through `ToolRunner` (wrong kind of tool).
- Letting the loop run without a cap (Module 5 already taught this).
- Treating hosted citations as owned `chunk_id`s in recall@k.
- Calling live `web_search` from CI.

## 6. Exercises

1. **Guided:** `first_turn`, `second_turn`.
2. **Open:** `run_two_steps`, `citation_line`.

```bash
uv run pytest concepts/a_05
```

- Hint 1: `next_hosted_turn(0, …)` then `(1, …)`.
- Hint 2: `"cited: " + ",".join(turn.citations)` or `"cited: none"`.
- Solution: `solutions/loop.py`, `solutions/output.py`.

## 7. Check

1. Who runs hosted file_search — you or the platform?
2. Why is Module 3 dispatch a misleading analog?
3. Predict: step 2 → exception or another search?
4. Are hosted citation ids the same as Module 4 `chunk_id`s?
5. Does the fake search the public web?

## Setup / troubleshooting

- `LLM_PROVIDER=fake`. No hosted tool network in CI.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** you can *explain* a hosted turn in an interview without depending on one in CI.

**What you learned:** hosted tools are platform-run; fake them in two steps and cap.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
