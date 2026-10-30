# A.6 Lock-in decision record   [NEW — no Java equivalent] [cost: mock] [~40 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/a_06/tests/test_skip.py` passes. **Still recommended.**

Official docs: [file_search](https://platform.openai.com/docs/guides/tools-file-search). Helper: `course_kit.hosted.decision_record`. Portfolio: Module 7 README.

## 1. Concept

A **decision record** is a short JSON/ADR blob: stack choice, recall, overlap, lock-in flags, `api=responses`, `assistants=False`. It belongs next to the capstone threat model. It is not a vendor comparison blog post.

## 2. Intuition

Flags that matter:

- `vendor_chunking` — you cannot unit-test the splitter
- `exportable` — can you leave with your index?
- `billed_separately` — retrieval $ on top of tokens
- `ci_honest` — `exportable and not vendor_chunking`

Owned RAG is `ci_honest`. Hosted file_search in this course is not.

## 3. Why it exists

Module 7 asks for known limitations. "We used hosted search because it was easy" is not a limitation you can defend. Write the choice down with numbers.

### The Java analogy that misleads you

An ADR in a Spring shop often picks a database. Hosted LLM retrieval is closer to "we outsourced the query planner". The analog is the *record*, not the product.

## 4. Step-by-step examples

**Example 1 — hosted flags.** vendor chunking + not exportable → `ci_honest=False`.

**Example 2 — we still pick own** when recall is 0.8 and we can eval.

**Example 3 — pasteable record.** `assistants` is always `False`.

**Example 4 — flags travel** inside `record["flags"]`.

**Example 5 — not legal advice.** Engineering only.

```bash
uv run python concepts/a_06/examples.py
```

## 5. Common pitfalls

- Picking hosted in CI because a demo looked good.
- Omitting `assistants: false` after the 2026-08-26 sunset.
- Recording a choice with no recall number.
- Treating `ci_honest` as a live SLA.

## 6. Exercises

1. **Guided:** `flags(...)`.
2. **Open:** `make_record(decision, flags)`.

```bash
uv run pytest concepts/a_06
```

- Hint 1: `ci_honest = exportable and not vendor_chunking`.
- Hint 2: `decision_record` already sets `api` and `assistants`.
- Solution: `solutions/lockin.py`, `solutions/record.py`.

## 7. Check

1. What makes a retrieval stack CI-honest?
2. Why keep `assistants: false` on the record?
3. Predict: vendor_chunking=True, exportable=False → `ci_honest`?
4. Is this record a contract with OpenAI?
5. Where does it go in the capstone?

## Setup / troubleshooting

- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** paste the dict into `modules/7-capstone/PORTFOLIO.md` under limitations.

**What you learned:** write the hosted-vs-own choice down; hosted is not CI-honest here.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
