# Technical Review — OpenAI APIs for the course
Docs checked 2026-10-29. Labels: [Verified] = read in official source on that date; [Proposed]; [Unverified].

Sources:
- S1 https://platform.openai.com/docs/guides/migrate-to-responses
- S2 https://pypi.org/pypi/openai/json (official `openai` package README/metadata)
- S3 https://platform.openai.com/docs/pricing
- S4 https://platform.openai.com/docs/guides/embeddings
- S5 https://platform.openai.com/docs/guides/conversation-state

## 1. Repo status
[Verified] The repo contains **no OpenAI/LLM-vendor SDK code**; only a local Ollama `/api/chat` call via `urllib` with `format: "json"` and Pydantic validation. Therefore **no deprecated OpenAI patterns are present**. Risk is in *future* lessons copying older tutorials (e.g. `openai.ChatCompletion.create` from SDK 0.x, Assistants API).

## 2. Python SDK (S2) [Verified]
- Latest PyPI `openai` = **3.41.0**, requires Python ≥3.10, Apache-2.0. HTTP layer is **HTTPX2**; sync `OpenAI` and async `AsyncOpenAI` clients.
- README states: "The primary API … is the Responses API"; Chat Completions is "the previous standard (supported indefinitely)".
- Reads `OPENAI_API_KEY` from env by default; recommends python-dotenv/.env. Responses are Pydantic models (`to_json()`, `to_dict()`); request params are TypedDicts.
- Retries: 2 by default (connection errors, 408, 409, 429, ≥500); default timeout 10 min; errors subclass `openai.APIError` (`RateLimitError`, `APIConnectionError`, …); `_request_id` exposed.
- Java analogy [Proposed]: like the official `openai-java` client (S1 shows Java builder examples) — `OpenAI()` ≈ a Spring bean configured from env; TypedDict params ≈ builder parameters; retries ≈ Spring Retry.

## 3. Chat Completions vs Responses (S1) [Verified unless marked]
| Aspect | Chat Completions `POST /v1/chat/completions` | Responses `POST /v1/responses` |
|---|---|---|
| Status | Supported; "Responses is recommended for all new projects" | Recommended |
| Input | `messages[]` | `input` (string or Items) + top-level `instructions` |
| Output | `choices[i].message.content`; `n` multiple choices | typed `output[]` Items (`message`, `reasoning`, `function_call`…); one generation; SDK helper `output_text` |
| State | Manual: resend full transcript | Manual replay of output Items, `previous_response_id` (with `store: true`), or Conversations API |
| Storage | Stored by default for new accounts | Stored by default; `store: false` to disable |
| Tools | Your own functions (externally tagged `{"type":"function","function":{…}}`), non-strict by default | Internally tagged `{"type":"function","name":…}`; strict attempted by default; hosted tools (web_search, file_search, code_interpreter, remote MCP, image generation, computer use) |
| Tool results | `tool` role message | `function_call_output` Item linked by `call_id` |
| Structured Outputs | `response_format: {type: json_schema, …}` | `text.format: {type: json_schema, …}` |
| Streaming | chunks with `delta` | typed SSE events (`response.output_text.delta`, `response.completed`, …) |
| Cost | — | OpenAI claims 40–80% better cache utilization in internal tests (vendor claim, not independently verified) |
- [Verified] "Even when using `previous_response_id`, all previous input tokens … are billed as input tokens." → server-side state ≠ free context. Key teaching point.
- [Verified] Per S1, starting with GPT-5.4, Chat Completions does not support tool calling with `reasoning_effort` other than `none`; some newest models require Responses for tool calling.
- [Verified] **Assistants API was sunset on August 26, 2026** (S1) — must not be taught.
- History [Verified only as stated in S1]: Responses is described as "an evolution of Chat Completions" incorporating Assistants-beta feedback. [Unverified] precise launch dates — check OpenAI changelog before writing the history section.
- Java analogy [Proposed]: Chat Completions ≈ stateless REST endpoint where the client holds the session (like passing full state each call); `previous_response_id` ≈ server-side HTTP session keyed by id; Items ≈ a sealed interface hierarchy (`sealed interface Item permits Message, FunctionCall, Reasoning`) handled with pattern-matching `switch`.

## 4. Embeddings (S4) [Verified]
`client.embeddings.create(model="text-embedding-3-small", input=...)` → `response.data[0].embedding`. Default dims 1536 (small) / 3072 (large); `dimensions` parameter shortens vectors; manual truncation requires re-normalization. Billed by input tokens.

## 5. Pricing & token accounting (S3) [Verified 2026-10-29, prices per 1M tokens]
- Examples: gpt-5-mini $0.25 in / $2.00 out / $0.025 cached; gpt-4.1-mini $0.40 / $1.60; text-embedding-3-small $0.02; text-embedding-3-large $0.13. Newer models have short/long-context tiers and cache-write prices.
- [Proposed] Course must never hard-code prices in prose; store them in `data/pricing.yaml` with source URL + date and compute from `response.usage` (input/output/cached tokens). Prices change frequently.
- [Unverified] reasoning-token billing details and tokenizer (`tiktoken`) specifics — not checked today; verify before lesson writing.

## 6. SDK vs frameworks vs hosted services [Proposed taxonomy]
- **SDK**: `openai` Python package — typed HTTP client (Spring `RestClient` analogy).
- **Hosted platform features**: Responses state/storage, Conversations API, hosted tools (web/file search, code interpreter), vector stores — run on OpenAI infra and may incur separate charges [Unverified: per-tool pricing].
- **Frameworks** (LangChain, LlamaIndex, OpenAI Agents SDK, etc.): orchestration libraries on top of SDKs ≈ Spring AI/LangChain4j. [Unverified] current versions/APIs — not checked.
- **Custom orchestration**: your own agent loop; the course should teach this first (repo's `mini_agent` already does) before frameworks.

## 7. Recommendations
[Proposed] Teach Responses first, Chat Completions as the widely-used legacy/compatible format (many providers incl. Ollama expose Chat-Completions-compatible endpoints [Unverified today]); one exercise migrating a Chat Completions snippet to Responses using S1's "common migration errors" checklist; fake client returns both shapes.
