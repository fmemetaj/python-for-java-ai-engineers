# Curriculum — Python for Java AI Engineers
Date: 2026-10-29. Owner: Curriculum Architect. Status: **[Proposed] — awaiting Federico's approval. Nothing implemented.**
Labels: **[Verified]** observed in repo/official docs on 2026-10-29 (see audit/technical-review) · **[Proposed]** design decision · **[Unverified]** assumption to validate.
Research refs: F1–F10 = `docs/research/market-research.md`; CM = `docs/research/competitor-matrix.md`; TR = `docs/technical/technical-review.md`; AUD = `docs/audit/repository-audit.md`.

## 1. Audience and prerequisites
- **Primary [Proposed]:** professional Java developers (≥2 yrs; Maven/Gradle, Spring or Jakarta EE, REST, JUnit, Git) who want to build LLM-backed features in Python. We do not re-teach programming (F4).
- **Secondary (later):** backend engineers from other typed languages (C#, Kotlin, Go). Java analogies stay, but each lesson must stand on its own without them.
- **Not targeted:** absolute beginners, ML researchers. Model training and fine-tuning are out of scope (CM: HF/fast.ai already cover them).
- **Machine:** Python 3.11–3.13 via uv, about 2 GB disk. A paid API key is **optional**. Every essential exercise passes with `LLM_PROVIDER=fake` (F8, AUD §5).

## 2. Design rules that apply to every module [Proposed]
1. One **running project**, *DocsDesk*: an assistant that answers questions about an internal Java/Spring service's docs and code. It grows module by module (F9).
2. We build on the plain SDK first. Frameworks come later and only as optional comparisons (F6, TR §6).
3. Engineering hygiene is part of the core: typed code, tests, retries, logging, cost tracking, and a small eval set from Module 2 onward (F5).
4. Reproducibility: committed `uv.lock`, model IDs and prices in config, a "last verified" stamp on each lesson (F1, TR §5).
5. Exercises are mainly `.py` files checked by pytest. Notebooks are optional explainers (F2: kernel friction).
6. Every lesson shows a cost badge: `mock` / `local` / `~$ with assumptions` (F8).

## 3. Module overview
Times are realistic first estimates for the target learner, covering reading plus exercises. **[Unverified]** until pilot learners record actual times (see course-strategy metrics).

| # | Module | Status | Essential? | Est. time (concepts + checkpoint) |
|---|---|---|---|---|
| 0A | Python Fundamentals I — core language (concepts 0.1–0.15) | [Proposed]; reuses existing notebooks 00/01/03 | Essential, fast-trackable per concept | 8–9 h |
| 0B | Python Fundamentals II — objects, typing, errors, runtime model (0.16–0.29) | [Proposed]; reuses notebooks 02/03/04/05/06 | Essential, fast-trackable | 8–9 h |
| 1 | Python Engineering & Tooling (uv, testing, HTTP, JSON, config) | [Proposed] | Essential | 6–7 h |
| 2 | LLM API Fundamentals | [Proposed] | Essential | 7–8 h |
| 3 | Structured Outputs, Tool Calling, First Evals | [Proposed] | Essential | 4–5 h |
| 4 | Embeddings, Semantic Search, RAG | [Proposed] | Essential (4.7 optional) | 6–7 h |
| 5 | Agents from Scratch | [Proposed] | Essential core; 5.5–5.6 optional | 5–6 h |
| 6 | Evals, Observability, Production | [Proposed] | Essential core; 6.6 optional | 5–6 h |
| 7 | Capstone: DocsDesk v1.0 | [Proposed] | Essential (portfolio) | 8–12 h |
| A | Electives | [Proposed] | Optional | 2–3 h each |

Times come from the concept map (§6) plus about 10% for module checkpoints. **[Unverified]** until pilot learners record actual times. Full path: about 58–69 h. An experienced Java dev who passes placement for most of 0A skips about 6–8 h of it.
**Change vs v1 of this plan (2026-10-29, after Federico's feedback):** Modules 0 and 1 are now a concept-by-concept fundamentals sequence. Every concept is taught Java-first when Java has an analog. Concepts with no Java equivalent are marked **NEW** and get more time. The existing notebooks are reused as material inside the concepts, not discarded.

## 3b. Teaching pattern for every concept (all modules, including AI) [Proposed]
- **Analog concept:** Concept → **Java version** (short snippet, ≤15 lines) → **Python version** side by side → **Differences & pitfalls** (where the analogy breaks) → exercise → check. Typical 20–45 min.
- **NEW concept — no Java equivalent:** Concept → **intuition** (plain-language mental model) → **why it exists** (problem it solves, what Java does instead) → **step-by-step examples** (3–5, growing) → exercises (≥2) → check. Typical 35–60 min, about 1.5× an analog concept.
- **Partial analogs** (e.g. annotations vs decorators, try-with-resources vs context managers, `Iterator` vs generators, CompletableFuture vs asyncio) are treated as NEW. The lesson opens with "the Java analogy that misleads you" so the learner doesn't over-trust it.

## 4. Placement and fast-track [Proposed] (F4)
`placement/self_check.py` holds a 15-minute check of 10 small tasks graded by pytest, all offline.
| If you can… | Skip to |
|---|---|
| Per-concept check: each 0.x concept has a 2–3-minute test; pass it → skip that concept (NEW concepts are recommended even if passed) | next concept |
| Pass all of 0A + 0B checks (incl. existing readiness check 06) | Module 1 |
| Also: set up a uv project with locked deps, call a JSON API with httpx and timeouts/retries, and load config from env | Module 2 |
| Also: have shipped an LLM API call with token/cost accounting | Module 3, after reading lesson 2.4 (Responses vs Chat Completions) |
| Already ship RAG in production | Modules 6 and 7. M4 and M5 are reference material. |
Every module also starts with a 3-question "do I need this?" check.

---
## Module 0A — Python Fundamentals I: Core Language
- **Objective:** write correct, idiomatic Python for everyday logic, understanding each construct relative to its Java counterpart or as a new idea.
- **Audience/prereqs:** Java developers; no Python needed.
- **Concepts in order:** 0.1–0.15 (see the concept map, §6). It starts with the familiar analogs (running code, variables, types, control flow, functions), then introduces the NEW ideas as soon as they're needed: truthiness, `*args/**kwargs`, scope/closures, slicing/unpacking, comprehensions, generators. Streams vs comprehensions comes last, as a bridge back to Java.
- **Reused [Verified exists]:** notebook 00 (getting started → 0.1/0.2), 01 Pythonic essentials (→ 0.5, 0.7, 0.11–0.13), 03 generators part (→ 0.14).
- **Exercises (examples):** port a Java `for` loop + `Map` aggregation to a comprehension. Fix the mutable-default-argument bug. Write a generator that streams log lines lazily. Rewrite a Java Stream pipeline 3 ways and choose the most readable.
- **Deliverable:** `fundamentals/log_stats.py`, a typed log-file analyzer passing provided tests.
- **Acceptance:** all 0.1–0.15 checks pass; the learner can explain when a generator beats a list and why `def f(x=[])` is a bug.
- **Why:** F3 ("Java in Python syntax", over-use of classes), F4 (fast-track per concept for experienced devs), Federico's directive to start from fundamentals.

## Module 0B — Python Fundamentals II: Objects, Typing, Errors, Runtime Model
- **Objective:** design Python code the Pythonic way rather than the Java way: data classes, protocols, type hints, exceptions, context managers, decorators, modules, and the concurrency model.
- **Concepts in order:** 0.16–0.29. Classes → properties → dunder methods (NEW) → dataclasses/Pydantic → inheritance → duck typing (NEW) → Protocols/ABCs → type hints vs generics → exceptions → context managers (NEW) → decorators (NEW) → modules/packages → threads → GIL & asyncio (NEW).
- **Reused:** notebooks 02 (typing/Pydantic/decorators), 03 (asyncio), 04 (modules, context managers), 05 mini agent (capstone of 0B), 06 readiness check.
- **Exercises (examples):** delete the getters/setters from a Java-style class using `@property`. Implement `__eq__`/`__repr__`/`__iter__` on a `Money` type. Replace an `interface` with a `Protocol` and make pyright catch a mismatch. Write a `@timed` decorator and a `@retry` decorator. Write a context manager that times a block. Run 10 fake I/O calls with `asyncio.gather` and compare against threads.
- **Deliverable:** existing `mini_agent` extended with a `Protocol`-typed tool registry and a decorator-based tool registration. Tests must pass.
- **Acceptance:** 0B checks + readiness check 06 pass; pyright clean; the learner can explain in their own words why decorators ≠ annotations and why asyncio doesn't make CPU code faster.
- **Why:** F3 (static-safety need → Protocols + type checker), AUD gaps (exceptions, Protocol depth), Federico's directive.

## Module 1 — Python Engineering & Tooling
- **Objective:** structure, build, configure, test, and integrate a Python service the way a Java engineer expects from Maven + Spring + JUnit.
- **Prereqs:** 0A/0B or placement.
- **Concepts in order:** 1.1–1.12 (the build tool first, then quality tooling, then runtime concerns). Only **one NEW** concept: virtual environments. Everything else maps cleanly to Java, so Module 1 moves fast.
- **Exercises:** convert a small Maven `pom.xml` mentally into `pyproject.toml` (given a template). Fix a broken lock/sync. Translate a JUnit 5 + Mockito test class into pytest + monkeypatch. Build an httpx client against a local mock server with timeouts and retries. Add a redacting log filter.
- **Project:** DocsDesk skeleton (package, settings, httpx client to a mock docs service, tests).
- **Acceptance:** `uv sync --locked && uv run pytest` green offline; pyright clean; a test asserts secrets never appear in logs.
- **Why:** F2 (setup friction; "you'll cry over not having Maven and Gradle"), F3, F5.

## Module 2 — LLM API Fundamentals
- **Pattern:** analogs (SDK client ≈ RestTemplate/WebClient, provider switch ≈ Spring profiles, state ≈ HTTP session, streaming ≈ Flux) are taught Java-first. Tokens, context window, sampling, cost, prompts-as-code, and reasoning are **NEW** and get deep explanations (concept map 2.1–2.11).
- **Objective:** call an LLM correctly and cheaply, and understand tokens, cost, state, and the two OpenAI API styles.
- **Prereqs:** M1. API key optional.
- **Lessons:**
  2.1 What an LLM call is: tokens, context window, sampling, nondeterminism (intuition, no math overload) + a short "why it works" sidebar (F9). 35–45 min
  2.2 Provider abstraction: the `LLMClient` Protocol with `fake`, `ollama`, and `openai` implementations ≈ interface + Spring profiles (architecture.md). 30–40 min
  2.3 Token economics: read `usage` and compute cost from `data/pricing.yaml` (dated, sourced; TR §5). Covers cached tokens. 40–50 min
  2.4 **Responses vs Chat Completions:** history, request/response shapes, Items as a sealed hierarchy, streaming events, `store`, portability, and when to use each. The same task is built both ways (F7, TR §3). 60–75 min
  2.5 Conversation state: manual replay vs `previous_response_id` vs Conversations API. **All prior input tokens are still billed** (TR §3 [Verified]). Truncation and summarization strategies. 45–60 min
  2.6 Prompts as code: instructions, templates, versioning prompts in files, and a first 5-case eval in pytest (F5). 40–50 min
  2.7 Reasoning models: effort settings, latency/cost trade-off, reasoning items. [Unverified details: reasoning-token billing per TR §5. Verify before writing.] 30–40 min
- **Exercises:** cost calculator with tests; migrate a Chat Completions snippet to Responses using the official checklist (TR §7); implement a context-budget trimmer; debug a "why did my bill triple" scenario that is caused by state replay.
- **Project:** DocsDesk can answer from a pasted doc, prints tokens and $ per call, and keeps a multi-turn session. Runs fully on the fake provider.
- **Acceptance:** works with `LLM_PROVIDER=fake` in CI. Cost calculation matches hand-computed fixtures. The learner can state 3 differences and 1 cost implication between the two APIs.
- **Why:** F7 (a real confusion), F8 (cost surprises), F1 (outdated API patterns: we teach the current SDK 3.x and no Assistants API, which was sunset 2026-08-26 per TR [Verified]).

## Module 3 — Structured Outputs, Function Calling, First Evals
- **Pattern:** structured outputs ≈ Jackson DTO + Bean Validation and tool calling ≈ interface dispatch/command pattern are taught Java-first. The tool-call loop and evals are **NEW** (3.1–3.5).
- **Objective:** get reliable typed data out of models and let models call your code safely.
- **Prereqs:** M2.
- **Lessons:**
  3.1 Structured outputs: JSON Schema from Pydantic, `text.format` (Responses) vs `response_format` (Chat Completions), and validation failures. 45–55 min
  3.2 Function calling, step by step: tool definitions, `function_call` → `function_call_output` by `call_id`, and the loop drawn as a sequence diagram (TR §3). 60 min
  3.3 Tool safety: argument validation, allow-lists, approval gates (reuses M0 05 `mini_agent`), idempotency. 40 min
  3.4 Evals 101: golden sets, exact/schema/rubric checks, running evals in pytest, regression on prompt change (F5). 45–60 min
- **Exercises:** extract a typed `Incident` from log text; add a `search_docs` tool; write a test that fails when the model calls a tool with invalid args (scripted fake).
- **Project:** DocsDesk returns typed answers with citations and can call `search_docs` / `get_endpoint_spec` tools.
- **Acceptance:** an eval set of ≥15 cases passes on fake; with a live key the pass rate is reported (no fixed threshold claimed); invalid tool args are handled.
- **Why:** F5 (no-engineering-depth complaint), F6 (understand the SDK before frameworks), TR §3 (strict tools, tool formats).

## Module 4 — Embeddings, Semantic Search, RAG
- **Pattern:** almost entirely **NEW** (embeddings, similarity, chunking, RAG, retrieval evals). Only the vector index (≈ Lucene/Elasticsearch) is taught Java-first.
- **Objective:** build and *measure* a retrieval-augmented system over a real Java codebase's docs.
- **Prereqs:** M3. numpy basics are introduced in place.
- **Lessons:** 4.1 Embeddings with real but small math: cosine, dimensions, normalization (TR §4) (F9 toy-with-real-math) · 4.2 Chunking: by size vs structure-aware (Markdown/Javadoc), metadata · 4.3 In-memory vector search with numpy, then when to use a vector DB · 4.4 RAG pipeline: retrieve → assemble context → answer with citations · 4.5 Retrieval evals: recall@k, groundedness checks · *4.6 Advanced: hybrid BM25 + vectors, reranking* · *4.7 Advanced: hosted file_search vs own pipeline (cost and lock-in)*. About 60 min each for 4.1–4.5.
- **Java analogies:** the vector index ≈ a Lucene/Elasticsearch index; the embedding model ≈ a hashing/feature function; the pipeline ≈ a Spring service chain.
- **Exercises:** implement cosine top-k; fix a chunker that splits code blocks; raise recall@5 on a fixed question set.
- **Project:** DocsDesk answers over the docs of a sample Spring Boot repo, which we write ourselves as a public, original fixture.
- **Acceptance:** recall@5 and a groundedness score are reported by `uv run docsdesk eval`; the course runs offline with precomputed fixture embeddings.
- **Why:** F9 (the theory gap before RAG; production chunking/hybrid). CM opportunity: depth over breadth.

## Module 5 — Agents and Orchestration from Scratch
- **Pattern:** agent loop ≈ state machine and tracing ≈ Micrometer/OTel are taught Java-first. Workflow-vs-agent, memory, and MCP are **NEW**.
- **Objective:** write and debug an agent loop you fully understand, and know when *not* to use an agent.
- **Lessons:** 5.1 Workflow vs agent (decision guide) · 5.2 The agent loop by hand: state, max steps, stop conditions · 5.3 Memory and context management · 5.4 Debugging and tracing agent runs (F5 "debug and measure") · *5.5 Optional: the same agent in one framework (selection decided at build time; versions [Unverified]), "what did it buy us?"* · *5.6 Optional: MCP tools.* 45–60 min each.
- **Java analogies:** the loop ≈ a state machine / Spring StateMachine; tools ≈ command handlers; traces ≈ distributed tracing spans.
- **Project:** DocsDesk "triage mode": a multi-step investigation with a human approval gate.
- **Acceptance:** a scripted fake replays a 5-step trajectory deterministically; agent evals check task success and step count; a step cap is enforced.
- **Why:** F6 (framework churn; demand for from-scratch resources), F5, CM (Ed Donner's agentic track was described as less technical).

## Module 6 — Evals, Observability, Production
- **Pattern:** observability, caching, and deployment are taught Java-first (Micrometer, @Cacheable, Spring Boot). LLM-as-judge, cost control, and prompt injection are **NEW**.
- **Objective:** make DocsDesk shippable: measured, observable, secure, and within budget.
- **Lessons:** 6.1 Eval strategy: offline sets, LLM-as-judge with calibration, regression gates in CI · 6.2 Observability: structured logs, OpenTelemetry spans, request IDs (`_request_id`, TR §2) · 6.3 Performance: streaming, async concurrency, timeouts, caching · 6.4 Cost control: budgets, model routing, prompt caching, a cost dashboard from logs · 6.5 Security: prompt injection, data leakage, secrets, tool permissions (OWASP LLM Top 10 [Unverified current version]) · *6.6 Advanced: deploy as a FastAPI service + container ≈ Spring Boot jar* · *6.7 Advanced: live smoke tests and SDK-upgrade drills (F1 "API change as a skill")*.
- **Acceptance:** a CI eval gate fails on an injected regression; an injection test suite passes; the per-request cost is logged.
- **Why:** F5 (evals as the gap; dedicated $4,400 evals course shows demand, CM), F8, F1.

## Module 7 — Capstone: DocsDesk v1.0
- **Objective:** a portfolio project defensible in an interview.
- **Options:** (a) DocsDesk over the learner's own (public) Java repo; (b) PR-review assistant for a Spring project; (c) log-triage assistant. A single brief per option, all original.
- **Deliverable:** repo with README, architecture diagram, eval report, cost report, threat model, and a 5-minute demo.
- **Acceptance (rubric):** runs from a clean clone with `uv sync --locked`; offline tests green; an eval report with ≥30 cases; documented cost per 100 requests; known limitations listed.
- **Why:** F9 (projects > certificates; one evolving project).

## 5. Removed or deferred topics [Proposed]
- Fine-tuning/QLoRA and model training are deferred: covered by Ed Donner/HF (CM), and they need a GPU (F8).
- Gradio UI stays as the existing optional demo only.
- A broad framework survey is dropped (F6).
- The Assistants API is excluded (sunset, TR).

## 6. Concept map [Proposed]
Kind: **Analog** = taught Java-first, side by side. **NEW** = no Java equivalent (partial/misleading analogs counted as NEW), with a longer deep explanation. Times are concept teaching + exercise time [Unverified estimates].
Totals: **76 concepts: 44 analog, 32 NEW.** Fundamentals (0A+0B): 17 analog, 12 NEW. Module 1: 11 analog, 1 NEW.

| ID | Concept | Java analog | Kind | Time | Module |
|---|---|---|---|---|---|
| 0.1 | Running Python: interpreter, REPL, scripts, `if __name__ == "__main__"` | `javac` + `public static void main`, JShell — No compile step; errors surface at runtime | Analog | 20 min | M0 |
| 0.2 | Notebooks (Jupyter) — cells, kernel, execution order | none — new — Hidden state from out-of-order cells; kernel selection (F2) | **NEW** | 25 min | M0 |
| 0.3 | Variables: names bound to objects, dynamic typing | Typed local variables / `var` — Rebinding vs mutation; no declarations | Analog | 30 min | M0 |
| 0.4 | Built-in types: int (unbounded), float, str (immutable), bool, None | Primitives + wrappers, `String`, `null` — `==` vs `is`; no int overflow; None ≠ null-safety | Analog | 30 min | M0 |
| 0.5 | Truthiness and falsy values | none — new — `if items:`; 0/''/[] are false | **NEW** | 20 min | M0 |
| 0.6 | Control flow: if/elif, for-in, while, `match` | if, enhanced for, while, `switch` patterns — No C-style for; `range`; for/else | Analog | 30 min | M0 |
| 0.7 | Functions: def, defaults, keyword args | Methods, overloading, builders — Mutable default argument trap | Analog | 35 min | M0 |
| 0.8 | `*args` / `**kwargs`, argument unpacking | none — new — Varargs is only a partial analog | **NEW** | 35 min | M0 |
| 0.9 | Scope (LEGB), closures, `nonlocal` | none — new — Block scope does not exist | **NEW** | 25 min | M0 |
| 0.10 | First-class functions and lambdas | Functional interfaces, lambdas, method refs — Python lambda = single expression | Analog | 25 min | M0 |
| 0.11 | Collections: list, dict, set, tuple | ArrayList, HashMap, HashSet, immutable List/record — Insertion-ordered dict; tuple immutability | Analog | 40 min | M0 |
| 0.12 | Slicing and unpacking (`a, *rest = …`) | none — new — Slices copy | **NEW** | 25 min | M0 |
| 0.13 | List/dict/set comprehensions | none — new — Readability limits; nesting | **NEW** | 45 min | M0 |
| 0.14 | Iterators, generators and `yield` | none — new — `Iterator<T>` is a partial analog; lazy, single-use | **NEW** | 50 min | M0 |
| 0.15 | Streams vs comprehensions/generators/itertools | `Stream` API (map/filter/collect) — No parallel streams; prefer comprehensions | Analog | 25 min | M0 |
| 0.16 | Classes and objects: `__init__`, `self`, no access modifiers | Classes, constructors, private/public — `_name` convention; no overloading of constructors | Analog | 45 min | M0 |
| 0.17 | Properties instead of getters/setters | Getters/setters, Lombok — Don't write getX() | Analog | 20 min | M0 |
| 0.18 | Dunder methods / data model (`__eq__`, `__repr__`, `__len__`…) | none — new — `toString/equals/hashCode` is a partial analog; operator protocol is new | **NEW** | 40 min | M0 |
| 0.19 | Dataclasses and Pydantic models | Records, Lombok, Jackson DTOs + Bean Validation — Runtime validation vs compile-time types | Analog | 35 min | M0 |
| 0.20 | Inheritance, MRO, multiple inheritance | extends / single inheritance — MRO and super() with multiple bases | Analog | 25 min | M0 |
| 0.21 | Duck typing | none — new — Behaviour over declared type | **NEW** | 30 min | M0 |
| 0.22 | Interfaces vs `Protocol` and ABCs | `interface`, `abstract class` — Structural vs nominal typing | Analog | 35 min | M0 |
| 0.23 | Generics vs type hints (`list[int]`, TypeVar, generics syntax), mypy/pyright | Generics, javac type checking — Hints are not enforced at runtime | Analog | 40 min | M0 |
| 0.24 | Exceptions: raise/except/finally, EAFP | Exceptions, try/catch/finally — No checked exceptions; exception chaining | Analog | 35 min | M0 |
| 0.25 | Context managers (`with`, writing your own via contextlib) | none — new — try-with-resources is a partial analog for *using* them; writing them is new | **NEW** | 40 min | M0 |
| 0.26 | Decorators | none — new — Annotations are a misleading analog: decorators execute code | **NEW** | 45 min | M0 |
| 0.27 | Modules, packages, imports | Packages, classpath, `import` — A file is a module; circular imports; `__init__.py` | Analog | 30 min | M0 |
| 0.28 | Threads and executors | `Thread`, `ExecutorService` — The GIL limits CPU parallelism | Analog | 25 min | M0 |
| 0.29 | GIL and the asyncio event loop: async/await, gather | none — new — CompletableFuture/WebFlux are partial analogs; cooperative scheduling is new | **NEW** | 60 min | M0 |
| 1.1 | uv: install Python, create projects, run | Maven/Gradle + SDKMAN — One tool for interpreter + deps | Analog | 40 min | M1 |
| 1.2 | pyproject.toml, dependency groups, `uv.lock` | pom.xml / build.gradle, scopes, lockfiles — Ranges vs locked versions | Analog | 25 min | M1 |
| 1.3 | Virtual environments (`.venv`) | none — new — Classpath is only a partial analog: per-project interpreter installs | **NEW** | 25 min | M1 |
| 1.4 | src layout, packaging, entry points | Maven layout, jar, `Main-Class` — Editable installs | Analog | 20 min | M1 |
| 1.5 | Linting/formatting/type checking: ruff, pyright | Checkstyle/Spotless, javac | Analog | 20 min | M1 |
| 1.6 | Logging | SLF4J/Logback — Module-level loggers; don't print | Analog | 20 min | M1 |
| 1.7 | Config and secrets: env, .env, pydantic-settings | `@ConfigurationProperties`, application.yml — Never log keys | Analog | 25 min | M1 |
| 1.8 | Testing with pytest: asserts, fixtures, parametrize | JUnit 5, `@BeforeEach`, `@ParameterizedTest` — Plain `assert`; fixture injection by name | Analog | 45 min | M1 |
| 1.9 | Mocking: monkeypatch, unittest.mock, respx | Mockito, WireMock — Patch where it's looked up | Analog | 30 min | M1 |
| 1.10 | HTTP with httpx (sync/async), timeouts | RestTemplate/RestClient, WebClient — Default timeouts differ | Analog | 40 min | M1 |
| 1.11 | JSON ↔ Pydantic models | Jackson + Bean Validation | Analog | 30 min | M1 |
| 1.12 | Retries with backoff | Spring Retry / Resilience4j | Analog | 25 min | M1 |
| 2.1 | LLM client (SDK) configured from env | RestTemplate/WebClient bean | Analog | 25 min | M2 |
| 2.2 | Tokens and tokenization | none — new — Not words; billing unit | **NEW** | 40 min | M2 |
| 2.3 | Context window and model limits | none — new | **NEW** | 30 min | M2 |
| 2.4 | Sampling, temperature, nondeterminism | none — new — Tests can't assert exact text | **NEW** | 35 min | M2 |
| 2.5 | Provider abstraction (fake/ollama/openai) | Interface + Spring profiles / @Primary test bean | Analog | 30 min | M2 |
| 2.6 | Token economics and cost calculation | none — new — Metered cloud billing is only a loose analog | **NEW** | 45 min | M2 |
| 2.7 | Chat Completions vs Responses API | Stateless REST vs server-side session — Stored state still bills all input tokens (TR) | Analog | 75 min | M2 |
| 2.8 | Conversation state and context trimming | HTTP session state | Analog | 45 min | M2 |
| 2.9 | Streaming responses | SSE / Flux — Typed events | Analog | 30 min | M2 |
| 2.10 | Prompts as versioned code + first eval | none — new | **NEW** | 45 min | M2 |
| 2.11 | Reasoning models and effort settings | none — new — Billing details [Unverified] | **NEW** | 35 min | M2 |
| 3.1 | Structured outputs (JSON Schema from Pydantic) | Jackson DTO + Bean Validation — Model may still refuse/fail | Analog | 50 min | M3 |
| 3.2 | Function/tool calling | Interface dispatch / command pattern | Analog | 45 min | M3 |
| 3.3 | The tool-call loop (call_id, outputs) | none — new — Model decides control flow | **NEW** | 40 min | M3 |
| 3.4 | Tool safety: validation, allow-lists, approval | Input validation, Spring Security authorization | Analog | 40 min | M3 |
| 3.5 | Evals: golden sets, rubric checks | none — new — JUnit is a partial analog; outputs are probabilistic | **NEW** | 55 min | M3 |
| 4.1 | Embeddings and vector spaces | none — new | **NEW** | 60 min | M4 |
| 4.2 | Cosine similarity and normalization | none — new | **NEW** | 40 min | M4 |
| 4.3 | Chunking and metadata | none — new | **NEW** | 50 min | M4 |
| 4.4 | Vector index / search | Lucene / Elasticsearch index | Analog | 45 min | M4 |
| 4.5 | RAG pipeline with citations | none — new | **NEW** | 60 min | M4 |
| 4.6 | Retrieval evals (recall@k, groundedness) | none — new | **NEW** | 50 min | M4 |
| 4.7 | Advanced: hybrid search + reranking | Elasticsearch BM25 scoring — optional | Analog | 60 min | M4 |
| 5.1 | Workflow vs agent decision | none — new | **NEW** | 35 min | M5 |
| 5.2 | Agent loop, max steps, stop conditions | State machine (Spring StateMachine) — Model-driven transitions | Analog | 60 min | M5 |
| 5.3 | Agent memory and context management | none — new | **NEW** | 45 min | M5 |
| 5.4 | Tracing and debugging agent runs | Distributed tracing (Micrometer/OTel) | Analog | 45 min | M5 |
| 5.5 | Optional: one framework comparison | Spring AI / LangChain4j — optional | Analog | 60 min | M5 |
| 5.6 | Optional: MCP tools | none — new — optional | **NEW** | 45 min | M5 |
| 6.1 | Eval strategy, LLM-as-judge, CI gates | none — new | **NEW** | 60 min | M6 |
| 6.2 | Observability: logs, spans, request IDs | Micrometer/OTel, MDC | Analog | 45 min | M6 |
| 6.3 | Performance: async concurrency, caching, timeouts | Caffeine/@Cacheable, thread pools | Analog | 45 min | M6 |
| 6.4 | Cost control: budgets, routing, prompt caching | none — new | **NEW** | 45 min | M6 |
| 6.5 | Security: prompt injection, data leakage | none — new — SQL injection is only a partial analog | **NEW** | 60 min | M6 |
| 6.6 | Advanced: FastAPI service + container | Spring Boot app + jar/container — optional | Analog | 60 min | M6 |
