# Maintainer and planning docs

This folder is **not** the learner path. Learners start at [Lesson 00](../notebooks/00_getting_started.ipynb).

The documents below are a **2026-10-29** snapshot of research and a proposed expansion from a one-hour Java→Python bridge into a longer, offline-first AI-engineering course. Status labels inside the files (`[Verified]`, `[Proposed]`, `[Unverified]`) still apply.

**Shipped now:** seven notebooks (estimated ~60 minutes for experienced Java developers), optional Gradio/Ollama lab, tests, and CI.

**M-1 hygiene (this repository):** committed `uv.lock`, Python 3.11–3.13 CI, Gradio tests skipped when Gradio is not installed, `ruff format --check`, non-blocking pyright, Dependabot, issue/PR templates, and estimated-time wording with a feedback form.

**Not started:** the Module 0A–7 rebuild, `course_kit`, DocsDesk, and placement checker described in the planning docs.

| Document | Purpose |
| --- | --- |
| [planning/course-strategy.md](planning/course-strategy.md) | Vision, principles, success metrics |
| [planning/curriculum.md](planning/curriculum.md) | Proposed modules and concept map |
| [planning/learning-experience.md](planning/learning-experience.md) | Lesson templates and exercise types |
| [planning/architecture.md](planning/architecture.md) | Proposed repository layout |
| [planning/implementation-roadmap.md](planning/implementation-roadmap.md) | Milestones; M-1 is the first code PR |
| [planning/community-growth.md](planning/community-growth.md) | Onboarding, issue forms, outreach (approval-gated) |
| [audit/repository-audit.md](audit/repository-audit.md) | Snapshot of `main` on 2026-10-29 |
| [quality/course-review.md](quality/course-review.md) | QA rubric and Module 0 review |
| [technical/technical-review.md](technical/technical-review.md) | OpenAI API notes for *future* lessons |
| [research/market-research.md](research/market-research.md) | Evidence F1–F10 |
| [research/competitor-matrix.md](research/competitor-matrix.md) | Public-course comparison |

Outreach, paid APIs, and GitHub Settings (branch ruleset, secret scanning) are **not** done by these files. The maintainer still has to enable protection on `main`.
