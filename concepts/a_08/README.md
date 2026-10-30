# A.8 SDK-upgrade drill: detect sunset APIs   [NEW — no Java equivalent] [cost: mock] [~50 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/a_08/tests/test_skip.py` passes. **Still recommended.**

Official docs: [Migrate to the Responses API](https://platform.openai.com/docs/guides/migrate-to-responses). Assistants sunset **2026-08-26** (technical-review.md). Helper: `course_kit.upgrade.scan_source`.

## 1. Concept

An **upgrade drill** scans source for strings that must not ship: `openai.ChatCompletion.create` (removed 0.x helper), `beta.assistants`, `client.beta.threads`, the words `Assistants API`. Current `client.chat.completions.create` is **still supported** (Module 2 taught it as the legacy shape). New work uses Responses.

## 2. Intuition

This is grep with reasons, not a compiler. Line numbers are 1-based. Clean Responses snippets return no findings.

```
openai.ChatCompletion.create  → legacy-0x
client.beta.threads           → sunset
client.responses.create       → ok
client.chat.completions.create → ok (not the 0.x helper)
```

## 3. Why it exists

API change is a skill (F1). Tutorials still paste Assistants and 0.x helpers. A 20-line scanner catches them before CI.

### The Java analogy that misleads you

`jdeps` / Error Prone catch *Java* APIs. They will not see a Python string `beta.assistants`. Treating this as "just bump the Maven BOM" misses the sunset.

## 4. Step-by-step examples

**Example 1 — Responses is clean.**

**Example 2 — 0.x helper is flagged** on line 1.

**Example 3 — threads are sunset.**

**Example 4 — current Chat Completions is allowed** (migration lesson still exists).

**Example 5 — honesty.** The scanner cannot migrate a live SDK for you; it catches strings.

```bash
uv run python concepts/a_08/examples.py
```

## 5. Common pitfalls

- Flagging `client.chat.completions.create` as sunset (it is not).
- Copying Assistants "threads" samples from old blogs.
- Assuming a major-version bump rewrites your calls.
- Running the drill against a live key "to see if it still works".

## 6. Exercises

1. **Guided:** `findings`, `is_clean`.
2. **Open:** `classify` → `ok` / `sunset` / `legacy-0x`.

```bash
uv run pytest concepts/a_08
```

- Hint 1: reuse `scan_source` / `sunset_free`.
- Hint 2: if any finding reason mentions Assistants or threads → `sunset`.
- Solution: `solutions/scan.py`, `solutions/migrate.py`.

## 7. Check

1. When was Assistants sunset?
2. Is `client.chat.completions.create` the 0.x helper?
3. Why is jdeps a misleading analog?
4. Predict: `# Assistants API was sunset` → classify?
5. Does this drill call OpenAI?

## Setup / troubleshooting

- `LLM_PROVIDER=fake`. This lesson is string matching.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** paste a blog snippet into the scanner before it enters DocsDesk.

**What you learned:** grep for sunset strings; Responses is ok; Assistants is not.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
