# Coverage and editorial audit

This document maps the independent course to the **topics listed** in the [Ed Donner LLM Engineering guides](https://github.com/ed-donner/llm_engineering/tree/main/guides). It **does not reproduce** his materials and does not claim all linked external ChatGPT tutorials were reviewed in full. Content and examples here are original.

| Ed Donner guide/topic | Status in this course | Location |
|---|---|---|
| 06: Python imports, functions/defaults | Covered with focused explanations | Lessons 01, 04; Guide 07 |
| 06: Strings, slicing, split/join, f-strings | Covered | Lesson 01; Guide 07 |
| 06: Lists, dicts, sets | Covered with exercises | Lesson 01 |
| 06: Files, Path, glob | Core essentials + optional detail | Lesson 04; Guide 07 |
| 06: Classes | Covered with Java analogies | Lesson 02 |
| 06: Pickle vs JSON | Optional security-oriented explanation | Guide 07 |
| 06: NameError in notebooks | Covered | Lesson 00; Guides 05, 07 |
| 10: Comprehensions | Covered and practiced | Lesson 01 |
| 10: Generators and yield | Covered, sync and async | Lesson 03 |
| 10: Subclasses/type hints/Pydantic | Relevant typing/Pydantic in core; inheritance optional | Lesson 02; Guide 07 |
| 10: Decorators | Covered, including a tool registry | Lesson 02 |
| 10: Docker | Optional note only | Guide 07 |
| 11: Async/await/gather; module entrypoint | Covered, with runnable I/O simulation | Lesson 03 |
| 04: API/client concepts, environment vars, uv | Only Python-relevant parts | Lesson 04; Guides 05, 07 |
| 04: Networking, screenshots, deeper SSL troubleshooting | Excluded from core: not Python language essentials | External guides as needed |

**Editorial standard:** Each notebook should explain motivation, include a short Java starting point, have several runnable experiments, prompt a learner prediction or exercise, and conclude with a checkpoint and optional guide links. README durations are **unmeasured estimates** for experienced developers, not a timed cohort result.

**Technical validation:** CI installs with `uv sync --locked` and runs ruff, pyright, pytest, and `pytest --nbmake` on Python 3.11–3.13 across Ubuntu, macOS, and Windows. The Gradio/Ollama live model quality is not tested in CI; Ollama integration is tested with mocked HTTP responses.
