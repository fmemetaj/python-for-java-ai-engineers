# A.2 Screenshot-to-answer for a Java stacktrace   [NEW — no Java equivalent] [cost: mock] [~50 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/a_02/tests/test_skip.py` passes. **Still recommended.**

Official docs: [Images and vision](https://platform.openai.com/docs/guides/images-vision). DocsDesk: `docsdesk.vision.VisionDesk`.

## 1. Concept

**Screenshot-to-answer** turns a catalogued image (a Spring stacktrace, a 401 page) into a DocsDesk answer with a request id and a cost. The fake reads the **description string**, not pixels.

## 2. Intuition

OCR + LLM is the live path. This course's fake is a lookup table: fixture id → description → canned answer. That is enough to wire the Responses item list, the prompt, and the log fields.

```
fixture id → description → FakeLLM.complete → catalog answer
                         ↘ usage + request_id
```

## 3. Why it exists

On-call Java engineers paste screenshots into Slack. A DocsDesk that only accepts Markdown misses that channel. You still need citations (the fixture id) and you still must not fetch random URLs.

### The Java analogy that misleads you

`ImageIO.read` plus a classifier is *your* computer vision. An LLM vision call is a billed API with a content list. Do not wrap `BufferedImage` and expect the SDK to "just take it".

## 4. Step-by-step examples

**Example 1 — refund 500.** `VisionDesk().ask_screenshot("stacktrace-refund-500", "Why 500?")` mentions NPE at `RefundService.java:42`.

**Example 2 — request id.** Same Module 6 field (`req_fake_…`), not `response.id`.

**Example 3 — items attached.** The result keeps the `input_text` + `input_image` list.

**Example 4 — 401 fixture.** Missing `Authorization` header.

**Example 5 — honesty.** The fake cannot teach JPEG artifacts, tiny fonts, or OCR errors. Live vision is optional via `.env`.

```bash
uv run python concepts/a_02/examples.py
uv run docsdesk vision
```

## 5. Common pitfalls

- Asserting on live OCR in CI.
- Forgetting the fixture id on the answer.
- Logging the raw screenshot bytes (or a data URL with a key in the query string).
- Pointing `image_url` at production hosts from tests.

## 6. Exercises

1. **Guided:** `fixture_description`, `fake_prompt`.
2. **Open:** `ask_refund_stacktrace`, `mentions_npe`.

```bash
uv run pytest concepts/a_02
```

- Hint 1: `get_fixture(id).description`.
- Hint 2: `VisionDesk().ask_screenshot("stacktrace-refund-500", …)`.
- Solution: `solutions/describe.py`, `solutions/ask.py`.

## 7. Check

1. What does the fake actually "see"?
2. Why keep `request_id` on a vision answer?
3. Is `ImageIO.read` a complete analog?
4. Predict: unknown fixture id — `KeyError` or empty string?
5. Does `uv run docsdesk vision` need a paid key?

## Setup / troubleshooting

- `LLM_PROVIDER=fake` (default). A live key is optional and never committed.
- Wrong API: `client.responses.create` only. No Assistants API.
- Windows: `set LLM_PROVIDER=fake`. PowerShell: `$env:LLM_PROVIDER="fake"`. macOS/Linux: `export LLM_PROVIDER=fake`.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** a Northwind refund 500 screenshot becomes a cited DocsDesk answer.

**What you learned:** fixture → prompt → FakeLLM usage; answers stay catalogued and offline.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
