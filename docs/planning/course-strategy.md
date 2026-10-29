# Course Strategy
Status: **[Proposed]**. Evidence: market-research.md (F1–F10), competitor-matrix.md (CM).

## Vision
A free, open-source, maintained course that takes a professional Java developer to shipping a measured, production-shaped LLM feature in Python. Over time, it should serve backend engineers in general.

## Positioning gap [Proposed, based on Verified sources]
- Popular free courses are broad and beginner-level, and their notebooks break when SDKs change (Microsoft repo issues #160/#544/#1060; Cookbook #933/#1463; Anthropic courses archived with retired model IDs). [Verified] (F1, CM)
- Paid project courses (e.g. Ed Donner's) are praised for projects. Reviews also report: Python is assumed from lecture one, extra API spend, "too easy" for experienced SWEs (single comment). [Verified sources, mixed strength] (F4, F8, CM)
- Evals, observability, and cost get thin coverage; dedicated evals courses exist to fill the gap. (F5)
- **Our niche:** Java-specific bridge + plain-SDK engineering depth + reproducibility + offline-first. We complement Ed Donner's courses and do not compete with or reproduce them.

## Principles
1. Value per hour over lesson count.
2. Original content only. Credit inspirations, never copy paid material.
3. Offline-first and cost-transparent.
4. SDK before framework. Label SDK vs hosted platform vs framework.
5. Reproducible: lockfile, CI, "last verified" stamps, model IDs and prices in config.
6. Java-first explanations that state where each analogy breaks.
7. Done = a learner can run it, complete a task, and demonstrate the skill.
8. Claims are labelled Verified/Proposed/Unverified; no success claims without data.

## Success metrics (collected only via opt-in, privacy-respecting means; no telemetry in code)
| Metric | Source | Target |
|---|---|---|
| Setup success rate | "setup report" issue form + `doctor.py` output pasted voluntarily | Baseline first; no target until ≥10 reports |
| Lesson completion / time taken | per-lesson feedback form (time spent, useful 1–5, confusion) | Compare actual vs estimated time; revise estimates when the gap is >30% |
| Exercise pass on first try | voluntary `course check` summary | Baseline |
| Confusion hotspots | feedback + Discussions Q&A tagged by lesson | Fix the top 3 per release |
| Technical errors | bug issues per lesson; CI nightly status | 0 open P1 breakages > 7 days |
| Project value | capstone showcase submissions | Qualitative |
| Contributor engagement | external PRs merged, first-time contributors | Tracked monthly |
Stars and forks are reported as reach only, not as quality (F10: upvotes/popularity ≠ quality).
