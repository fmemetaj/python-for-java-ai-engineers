# Course Review — QA Rubric and Module 0 Review
Date: 2026-10-29. Owner: QA Reviewer. The Module 0 review relies on the audit's executed results [Verified] plus the notebook structure. Pedagogical judgements are **[Proposed]** opinions, and no learner has validated them yet.

## Rubric (each criterion PASS/FAIL; a lesson ships only if every ★ criterion passes)
| # | Criterion | PASS when |
|---|---|---|
| ★1 | Technical correctness | Technical Expert signed off; APIs match docs on the stamped date; no deprecated patterns (Assistants API, `openai.ChatCompletion`) |
| ★2 | Reproducibility | Executes in CI from clean `uv sync --locked` on 3.11–3.13 with `LLM_PROVIDER=fake` |
| ★3 | Offline accessibility | Essential exercises pass with no key; live cost stated with a dated price source |
| ★4 | Active learning | ≥1 graded exercise that requires change/debug/implement; stubs fail and solutions pass the tests |
| ★5 | Java clarity | Analog concept: Java snippet first, then Python side by side, plus a differences/pitfalls table. NEW concept: marked "NEW — no Java equivalent", with intuition, why it exists, ≥3 step-by-step examples, ≥2 exercises. No "Java in Python syntax" in examples |
| 6 | Practical relevance | Real scenario tied to DocsDesk or a production failure mode |
| 7 | Understanding check | Knowledge check tests reasoning, not recall |
| 8 | Prereqs and time | Prereqs and "skip if" stated; time estimate present (validated later by feedback) |
| ★9 | Originality | No copied or paraphrased paid/proprietary material; sources credited |
| 10 | Navigation | Links valid; previous/next links; listed in README module table |
| ★11 | Security | No secrets; keys only via env; logs redact |
| 12 | Not doc-restating | Adds explanation, trade-offs, or exercises beyond the official docs |

## Module 0 review (existing notebooks 00–06)
| Criterion | Result | Notes / action |
|---|---|---|
| 1 Correctness | PASS | No vendor SDK code; Ollama via urllib with Pydantic validation [Verified] |
| 2 Reproducibility | **FAIL (minor)** | Notebooks 7/7 and pytest 15/15 pass on 3.11/3.12/3.13 [Verified], but there is no committed `uv.lock`, CI runs only 3.12, and default `--group dev` install → gradio test collection error. Fix: quick fixes 1–3 |
| 3 Offline | PASS | No keys needed |
| 4 Active learning | PASS (provisional) | Guided practice cells plus readiness check 06; but no stub-fails/solution-passes test separation → add during M-1/M0 |
| 5 Java clarity | PASS | Java-first rework commit; mapping guide 02 |
| 6 Relevance | PASS | 05 mini agent with approval gate |
| 7 Knowledge check | PASS (partial) | Only 06 has a quiz; add 2–3 questions per notebook |
| 8 Prereqs/time | **FAIL (minor)** | The "60 minutes" claim is unmeasured; no per-notebook times or skip guidance → add estimates + placement |
| 9 Originality | PASS (provisional) | States originality and only maps topics to Ed Donner's public guide list; text not diffed [Unverified] |
| 10 Navigation | PASS (improve) | Three overlapping nav docs; README long |
| 11 Security | PASS | Secret scan of tree and history clean; loopback-only Ollama [Verified] |
| 12 Beyond docs | PASS | Java mapping adds value |
**Verdict:** Module 0 is **keep, with minor fixes**. No ★ criterion fails on content; ★2 fails only on reproducibility hygiene, which the M-1 quick fixes resolve. Gaps to fill in M0: exceptions/logging idioms, Protocols, type checker.

**Note (2026-10-29):** under the new concept-by-concept structure, the existing notebooks become *source material* for concepts 0.1–0.29. They currently do not follow Template A/B (no consistent Java-snippet-first + pitfalls table; NEW concepts like generators and decorators are not given the deep treatment), so ★5 would be **FAIL** against the updated rubric until they are reworked in milestone F.
