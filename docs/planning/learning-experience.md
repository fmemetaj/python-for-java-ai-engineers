# Learning Experience Design
Status: **[Proposed]**. Owner: LX Designer. Based on F2, F4, F5, F8, F9 (market-research.md) and the existing Module 0 pattern [Verified: Java-first guided practice, Cursor "hints before solutions" rule].

## 1. Concept lesson templates (updated 2026-10-29 per Federico's feedback)
The course is a sequence of **concepts** (see curriculum.md §6 concept map). Each concept uses one of two templates.

### Template A — Concept WITH a Java analog
```
# 0.11 Collections   [Analog: ArrayList/HashMap/HashSet/record] [cost: mock] [~40 min] [last verified: date, Python 3.11–3.13]
Skip if: <2-minute check passes>
1. Concept         – what it is and the engineering problem it solves (2–4 sentences)
2. Java version    – short, compilable Java snippet (≤15 lines) the learner already knows
3. Python version  – equivalent idiomatic Python, shown SIDE BY SIDE with the Java one
4. Differences & pitfalls – table: "Java habit → Python reality → pitfall/bug it causes" (where the analogy breaks)
5. Exercise        – port/fix/implement; graded by `uv run pytest concepts/0_11`
6. Check           – 3–5 reasoning questions (predict output, spot the Java-ism)
(+ optional: real scenario, further challenge, what you learned — 1–3 lines each)
```

### Template B — NEW concept (no Java equivalent)
```
# 0.14 Generators and yield   [NEW — no Java equivalent] [cost: mock] [~50 min]
1. Concept         – one-sentence definition
2. Intuition       – plain-language mental model + diagram (e.g. a paused function)
3. Why it exists   – the problem it solves and what you'd do in Java instead (and why that's clunkier)
4. Step-by-step examples – 3–5 small runnable examples, each adding one idea
5. Common pitfalls – e.g. single-use iteration, lazy evaluation surprises
6. Exercises       – ≥2: one guided, one open (graded by pytest)
7. Check           – 3–5 reasoning questions
(+ optional: real scenario, further challenge, what you learned)
```
- If a Java analog is **partial or misleading** (annotations vs decorators, try-with-resources vs context managers, `Iterator` vs generators, CompletableFuture vs asyncio, JUnit vs evals, SQL injection vs prompt injection), use Template B. Add a "The Java analogy that misleads you" box after Intuition.
- The same templates apply to AI concepts: e.g. the LLM SDK client (A: vs RestTemplate/WebClient), structured outputs (A: vs Jackson DTO + Bean Validation), tool calling (A: vs interface dispatch), tokens/embeddings/RAG (B).
- Rules: no padding; a concept >60 min gets split; every code block (Java snippets compiled in CI with a JDK 21 step [Proposed]) is executed; no paid material is copied or paraphrased.
- Feedback link at the end of every concept (community-growth.md).

## 2. Exercise types (rotate them; do not just "run the cell")
| Type | Example | Grading |
|---|---|---|
| Predict | "What does `usage.input_tokens` show on turn 3?" | knowledge check |
| Fix the bug | the chunker splits a code fence | pytest |
| Implement | `cost_of(usage, model)` | pytest + hidden edge cases |
| Extend | add a tool to DocsDesk | pytest + eval set |
| Measure | improve recall@5 from baseline | metric threshold relative to baseline |
| Migrate | Chat Completions → Responses | pytest against both fake shapes |
| Review | critique a flawed design (Java-style over-engineering) | self-check rubric |

## 3. Mock/offline-first design [Proposed]
- `LLM_PROVIDER=fake|ollama|openai` (default `fake`). `FakeLLM` returns **Responses-shaped and Chat-Completions-shaped** objects from sanitized recorded fixtures, including `usage`, so cost exercises work offline.
- **Scripted fakes** for tool and agent lessons: a fixture lists the expected tool calls and returns canned outputs, so the loop runs deterministically.
- Embeddings: precomputed fixture vectors for the sample corpus; a fake hash-based embedder for unit tests.
- Exercises are graded on **your code's behavior** (parsing, loops, cost, validation), never on model wording, so they pass offline. Live runs are an optional "now try it for real" step with a stated cost.
- Ollama remains the free local path, bound to loopback (existing pattern). [Unverified] which small model is good enough for tool calling; to be tested in M2.
- Honesty: each fake-only lesson states what the fake cannot teach (latency, real variability).

## 4. Levels
- **Track markers:** 🟢 core (everyone) · 🔵 deeper (recommended) · 🟣 advanced/optional.
- **Fast track:** a 2–3-minute skip check per concept. Analog concepts can be skipped on pass. NEW concepts are recommended even on pass, because that's where Java devs get surprised.
- **Hints ladder** in exercises: hint 1 (concept) → hint 2 (API pointer) → solution in `solutions/` (validated in CI). This matches the existing Cursor tutor rule.
- **Self-paced checkpoints:** each module ends with `uv run course check mN`, which prints pass/fail per exercise.

## 5. Accessibility and cost
Cost badge on every lesson; "total live cost for this module ≈ $X at prices from data/pricing.yaml (date)". Diagrams get alt text. No video required.
