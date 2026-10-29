# Implementation Roadmap
Status: **[Proposed]** for Modules 0A–7. **M-1 is the first implementation PR** (lockfile, CI matrix, Gradio `importorskip`, ruff format, non-blocking pyright, Dependabot, issue/PR templates, estimated-time wording, and these planning docs). Remaining work still happens on branches → PR → CI → QA review → maintainer merge.

`.env.example` stays deferred until cloud-API lessons land. Branch ruleset and secret scanning are GitHub Settings work for the maintainer.

## Roles
| Role | Owns |
|---|---|
| Market Research | evidence updates, pilot-feedback analysis |
| Curriculum Architect | curriculum.md, objectives, sequencing, scope cuts |
| Technical Expert | API accuracy, pricing.yaml, fixtures, lesson tech sign-off, SDK-upgrade drills |
| LX Designer | lesson template, exercises, knowledge checks |
| Implementation Engineer | the only role that edits repo files; branches, code, tests, CI |
| QA Reviewer | course-review.md rubric; independent pass/fail per lesson |
| OSS Growth | README/onboarding, templates, Discussions, outreach drafts (approval-gated) |

## Quick fixes from the audit (M-1, first PR) [Verified issues → Proposed fixes]
1. `tests/test_gradio_demo.py` breaks collection under the default `uv sync --group dev` → add `pytest.importorskip("gradio")`.
2. Commit `uv.lock`; CI uses `uv sync --locked`.
3. CI matrix Python 3.11 / 3.12 / 3.13 (all pass locally per audit).
4. Add `ruff format --check`; add pyright (non-blocking at first).
5. Add `.github/dependabot.yml` (uv + actions), issue/PR templates.
6. Add `.env.example` (only once cloud lessons land).
7. README: shorten, add a "Start here" block and a placement link; merge or redirect overlapping nav docs (README/PROGRESS/guides README).
8. Replace the unmeasured "60 minutes" claim with "estimated; tell us your time".
9. Enable branch ruleset on `main` + secret scanning/push protection (GitHub settings, done by Federico).

## Milestones
| M | Deliverable | Depends on | Priority | Size |
|---|---|---|---|---|
| M-1 | Quick fixes above | approval | P0 | 0.5–1 day |
| M0 | `course_kit` foundation: `LLMClient` Protocol, FakeLLM (both API shapes), pricing.yaml + cost.py, fixture recorder, doctor.py, placement check; module folder layout (architecture.md) | M-1 | P0 | 3–4 days |
| F | Fundamentals 0A+0B: 29 concept lessons (17 analog, 12 NEW), reusing existing notebooks as material; JDK step in CI to compile Java snippets | M-1 | P0 | 8–10 days |
| M1 | Module 1 (12 concepts) + DocsDesk skeleton | M0, F | P0 | 5–6 days |
| M2 | Module 2 (11 concepts) incl. Responses vs Chat Completions | M0, Tech re-verification of reasoning billing + history dates | P0 | 6–8 days |
| M3 | Module 3 + eval harness | M2 | P0 | 4–5 days |
| **MVP release v0.1** | Modules 0–3, pilot with 3–5 volunteer Java devs | M3 + QA pass | — | — |
| M4 | Module 4 RAG + original sample Spring corpus | MVP feedback | P1 | 6–8 days |
| M5 | Module 5 agents | M4 | P1 | 5 days |
| M6 | Module 6 production | M5 | P1 | 6–8 days |
| M7 | Capstone briefs + rubric | M6 | P2 | 3 days |
| A | Electives | demand from feedback | P3 | — |
Sizes are agent-assisted effort estimates **[Unverified]**.

## MVP recommendation (revised 2026-10-29 after fundamentals rework)
**v0.1 "Fundamentals" = Modules 0A + 0B + 1** (about 22–25 h; 41 concepts, all offline, no AI cost). It ships first because it is self-contained, is directly what Federico asked for, and reuses the existing notebooks.
**v0.2 "First LLM feature" = + Modules 2 + 3** (cumulative about 33–38 h). It delivers DocsDesk v0.3 with typed answers, tools, cost tracking, and a 15-case eval, and it covers the strongest AI-side evidence (F5, F7, F8).
Previous MVP (Modules 0–3, 13–18 h) is superseded: the fundamentals sequence roughly triples Module 0's time.
Gates: QA passes every concept in the release; ≥3 pilot learners finish 0A and report times. If pilot times exceed estimates by >30%, re-cut before v0.2.

## Test requirements (every PR)
- Java snippets in concept lessons compile (JDK 21 in CI) [Proposed]
- `uv sync --locked`; pytest on 3.11–3.13; all notebooks/scripts executed with `LLM_PROVIDER=fake`; `solutions/` pass the exercise tests; exercise stubs *fail* the tests (guards against shipped solutions); ruff check + format; secret scan.
- Weekly: link check, Windows run, dependency-update PR.
- Manual `workflow_dispatch` live smoke with a capped key (needs Federico to create the secret and a spend limit).
- QA rubric pass (docs/quality/course-review.md) + Technical Expert sign-off before merge.
