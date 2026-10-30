# A.1 Image inputs on the Responses API   [NEW — no Java equivalent] [cost: mock] [~50 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/a_01/tests/test_skip.py` passes. **Still recommended.**

Official docs: [Images and vision](https://platform.openai.com/docs/guides/images-vision), [Responses API](https://platform.openai.com/docs/guides/migrate-to-responses). Course helpers: `course_kit.vision`.

## 1. Concept

A **vision call** is a Responses request whose `input` includes an `input_image` item (`image_url` plus `detail`) next to `input_text`. It is not a Chat Completions `image_url` content part, and it is not the sunset Assistants file API.

## 2. Intuition

The model does not open a `.png` on disk. You send a URL, a data URL, or — in this course — a **fixture id** (`fixture://stacktrace-refund-500`). The fake never fetches HTTP. It looks up the catalog row.

```
question (input_text) ─┐
fixture image item    ─┴─→ responses.create → output_text
```

## 3. Why it exists

Java services attach screenshots to tickets. DocsDesk should answer "why is this 500?" from that screenshot. There is no Servlet analog for "tokens that represent pixels".

### The Java analogy that misleads you

`multipart/form-data` file upload is how the *bytes* arrive at your server. It says nothing about how an LLM bills or shapes that image. Do not treat `Part.getInputStream()` as `input_image`.

## 4. Step-by-step examples

**Example 1 — catalog, not pixels.** `get_fixture("stacktrace-refund-500")` has width/height and a description. No PNG is in git.

**Example 2 — item type.** `{"type": "input_image", "detail": "low", "image_url": "fixture://…"}`.

**Example 3 — content list.** Text first, image second. `parse_image_ids` reads only `fixture://` URLs.

**Example 4 — https rejected.** Graded helpers raise `ValueError` on `https://example.com/x.png`. Live fetches are optional and never CI.

**Example 5 — a second fixture.** `auth-401-screenshot` is a missing Bearer header.

```bash
uv run python concepts/a_01/examples.py
```

## 5. Common pitfalls

- Using Chat Completions `image_url` parts on a Responses client.
- Fetching images in tests.
- Putting the screenshot in `instructions` instead of `input`.
- Assuming Assistants file ids still work (sunset 2026-08-26).

## 6. Exercises

1. **Guided:** `fixture_image_url`, `image_item`, `parse_fixture_ids`.
2. **Open:** `text_item` and `vision_content`.

```bash
uv run pytest concepts/a_01
```

- Hint 1: `type` is `input_image`, URL is `fixture://` plus the id.
- Hint 2: skip non-image items; reject anything that is not `fixture://`.
- Solution: `solutions/items.py`, `solutions/content.py`.

## 7. Check

1. What is the Responses item `type` for an image?
2. Why does this course forbid `https://` image URLs in graded work?
3. Is `multipart/form-data` a complete analog?
4. Predict: content list with only `input_text` — does `parse_fixture_ids` succeed?
5. Does this lesson call the Assistants API?

## Setup / troubleshooting

- `LLM_PROVIDER=fake` (default). A live key is optional and never committed.
- Wrong API: `client.responses.create` only. No Assistants API.
- Windows: `set LLM_PROVIDER=fake`. PowerShell: `$env:LLM_PROVIDER="fake"`. macOS/Linux: `export LLM_PROVIDER=fake`.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** Elective A2 feeds these items into DocsDesk vision.

**What you learned:** Responses `input_image` items; fixture URLs; no live fetches in CI.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
