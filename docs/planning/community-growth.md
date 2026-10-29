# Community Growth & Developer Experience
Status: **[Proposed]. Nothing is published, posted, or sent and no one is contacted without Federico's explicit approval.** Owner: OSS Growth.

## README / onboarding
- Top of README: a one-sentence promise, who it is for, a "Start here in 3 commands" block (`uv sync --locked`, `uv run doctor.py`, `uv run pytest`), a placement link, a module table with times and cost badges, and the status (what exists vs planned).
- Move long rationale into docs/. Keep honest disclaimers (estimates, not affiliated with Ed Donner, original content).
- Troubleshooting page: python vs python3, Jupyter kernel selection, corporate proxy/SSL, Windows long paths (F2).

## CONTRIBUTING (extend existing)
Fork → branch → PR only; contributors never get write access. Lesson template compliance; original work and no paid course material (DCO sign-off proposed); tests required; "last verified" stamp updates; code of conduct (Contributor Covenant). Maintainer duties: triage weekly, respond within 7 days (target), Federico is the sole merger.

## Issue templates (forms)
bug (lesson, OS, Python, `doctor.py` output) · lesson feedback · setup report · content proposal · API/SDK breakage · good-first-issue tasks.

## Lesson feedback mechanism
Each lesson ends with a link to a prefilled issue form: lesson ID, time spent, usefulness 1–5, the most confusing part, and whether it was completed. Optional and anonymous-friendly via Discussions. No tracking or telemetry in code.

## Discussions categories
Announcements (maintainer only) · Q&A (per-module labels) · Show and tell (capstones) · Ideas / curriculum proposals · Java→Python gotchas · Polls.

## Sharing channels (draft posts first; Federico approves each one)
- **LinkedIn** (Federico's own audience): build-in-public posts per milestone that show what was learned, not "please star".
- **GitHub:** topics/tags, a good README, pinned issues for first contributors; submission to relevant awesome-lists only where their contribution rules allow it.
- **Reddit:** read each sub's rules first. Many limit self-promotion (r/learnpython, r/Python, r/LocalLLaMA, r/learnmachinelearning) [Unverified current rules, check before any post]. Prefer answering existing questions where the course genuinely helps, with disclosure, or using designated showcase threads. Never cross-post blasts.
- Hacker News "Show HN" only at v1-quality; Java communities (r/java, local JUGs, dev.to) later.

## Early contributor strategy
Label 10–15 good-first-issues (fixture recording, knowledge-check questions, troubleshooting entries, Windows testing). Recruit 3–5 pilot learners from Federico's network for the MVP. Credit contributors in a CONTRIBUTORS file and the release notes. Prefer "translate a Java example to a different JVM language" style contributions.

## Adoption metrics
Setup-report success rate, lesson feedback count and usefulness, completions reported, external PRs merged, first-time contributors, issues resolved in time, plus reach (stars, forks, referrers from GitHub traffic) as context only.
