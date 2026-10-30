# Setup troubleshooting

Use this page when install, PATH, kernels, or downloads fail. For a one-shot local check:

```bash
uv run python scripts/doctor.py
```

Add `--offline` to skip the PyPI probe. Doctor never prints secret values; it only reports whether `OPENAI_API_KEY` is set.

The core notebooks do not need a paid API key. If a command below fails, fix that before opening Lesson 00.

## Install uv (Windows, macOS, Linux)

Official docs: [astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/).

**macOS / Linux**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Restart the terminal, or `source $HOME/.local/bin/env`, then confirm `uv --version`.

**Windows (PowerShell)**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

If `uv` is still not found, the installer directory is not on PATH (see below).

Then, from the repository root:

```bash
uv python install 3.12
uv sync --locked --group dev
uv run python scripts/doctor.py --offline
uv run jupyter lab
```

`--locked` installs the versions in `uv.lock`. If you changed `pyproject.toml`, run `uv lock` and commit the lockfile.

## `uv` or `python` not found (PATH)

Java analogy: this is the same class of problem as a JDK that is installed but not on `PATH`, so `javac` fails in a new shell.

1. Close and reopen the terminal after installing uv. GUI apps (Cursor, VS Code) inherit PATH from the time they were launched.
2. On **macOS/Linux**, uv usually lands in `~/.local/bin`. Add that directory to PATH, or `source ~/.local/bin/env`.
3. On **Windows**, uv usually lands in `%USERPROFILE%\.local\bin`. Add it in Settings → Environment variables, then restart the terminal **and** the editor.
4. Prefer `uv run python` over a system `python`. That uses the project's `.venv`.
5. If `python` is missing but `python3` works, that is normal on macOS/Linux. Use `python3` or `uv run python`.
6. On Windows, `py -3.12` is the [Python launcher](https://docs.python.org/3/using/windows.html#python-launcher-for-windows). The Microsoft Store `python` stub is not a working interpreter — doctor warns if it sees `WindowsApps` in the path.
7. Confirm: `uv python list` and `uv run python --version`.

## Jupyter kernel in Cursor / VS Code

The notebook kernel must be the same interpreter as `.venv`. Mixing this with a global Python is the usual cause of `ModuleNotFoundError: pydantic` or `mini_agent`.

1. Open the **repository folder**, not a single notebook.
2. Install the recommended **Python** and **Jupyter** extensions (see `.vscode/extensions.json`).
3. Command Palette → **Python: Select Interpreter** → `.venv\Scripts\python.exe` (Windows) or `.venv/bin/python` (macOS/Linux).
4. Open `notebooks/00_getting_started.ipynb`. In the kernel picker, choose that same `.venv`.
5. If the file opens as JSON, **Open With → Jupyter Notebook**.
6. If the kernel is missing, from the repo root:

```bash
uv run python -m ipykernel install --user --name java-ai-python --display-name "Python (java-ai-python)"
```

Then restart the editor and select **Python (java-ai-python)**.

Cursor is optional. `uv run jupyter lab` in a browser works without an IDE.

## Proxy, SSL inspection, and VPN

Corporate networks often intercept HTTPS (like a Java truststore that lacks the corporate CA).

- uv honors `HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`, and the lowercase variants. Doctor lists **variable names only**, not values (values may contain credentials).
- If TLS inspection breaks downloads, point `SSL_CERT_FILE` (and often `REQUESTS_CA_BUNDLE`) at your organization's CA bundle. Do not disable certificate verification.
- A **VPN** can block PyPI or force traffic through a proxy that uv does not know about. Try with VPN off, or set the proxy variables your IT team documents.
- `uv run python scripts/doctor.py` (without `--offline`) probes `https://pypi.org/simple/`. A WARN there is a network/TLS problem, not a Python syntax problem.
- Internal package indexes: configure uv via environment or config; do not put credentials in the repo.

## Windows extras

- Enable long paths if clone or sync fails on deep paths: `git config --global core.longpaths true`.
- Prefer PowerShell or Windows Terminal over an ancient `cmd.exe` that still has a pre-install PATH.
- If you use **WSL**, do the entire course inside WSL: clone, uv, `.venv`, and Jupyter all on the Linux side. Do not mix `C:\...` Python with `/home/...` notebooks.

## WSL

Run `uv` and the notebooks in the WSL distro. Open the Linux folder in Cursor/VS Code (`\\wsl$\...` or the WSL remote). A Windows `.venv` will not import correctly from Linux, and the reverse is also true.

## Apple Silicon (macOS)

Use the arm64 build of uv and CPython (`uv python install 3.12`). If you see **Bad CPU type in executable**, the current shell is running an x86_64 (Rosetta) binary. Open a native Terminal.app window, or `arch -arm64 zsh`, then reinstall uv.

Intel Macs are supported; times for the optional local model will be slower.

## Linux

You need a compiler toolchain only if a wheel is missing for your platform (uncommon on x86_64/aarch64 CPython 3.11–3.13). Install uv with the official script rather than an outdated distro package.

## Default tests vs the Gradio demo

```bash
uv sync --locked --group dev
uv run pytest -q
```

That default install **does not** include Gradio. Tests that import the optional app skip via `pytest.importorskip("gradio")`. To run them:

```bash
uv sync --locked --group dev --group demo
uv run pytest -q
```

## Module 1 (uv, lockfile, `.env`, HTTP)

- **Stale lock:** `uv lock` then commit both `pyproject.toml` and `uv.lock`. CI runs `uv sync --locked` and fails if they disagree.
- **`.env`:** copy `.env.example` to `.env` for local overrides. Never commit `.env`. Doctor reports whether `OPENAI_API_KEY` is set, not the value.
- **httpx hangs:** graded tests use `httpx.MockTransport` and must not call the network. Always pass `timeout=`.
- **`ModuleNotFoundError: docsdesk` / `httpx`:** `uv sync --locked --group dev` from the repository root, then `uv run python` (or select `.venv`).
- **Live OpenAI is optional:** keep `LLM_PROVIDER=fake`. If you opt in, use `client.responses.create` ([Responses API](https://platform.openai.com/docs/guides/migrate-to-responses)), never the sunset Assistants API.

## Module 2 (LLM calls, tokens, cost)

- **No key in CI:** graded work uses `FakeLLM`. `get_client("openai")` raises on purpose.
- **`usage` fields:** Responses uses `input_tokens` / `output_tokens`; Chat Completions uses `prompt_tokens` / `completion_tokens`.
- **Bill looks 3× too high:** `previous_response_id` still bills prior input tokens. Trim context (concept 2.8); do not assume a session id is free.
- **Prices:** read `data/pricing.yaml` (dated, sourced from [OpenAI pricing](https://platform.openai.com/docs/pricing)). Do not hard-code rates in code you will forget to update.
- **Old snippets:** `openai.ChatCompletion.create` and the Assistants API are out of scope.

## Module 3 (structured outputs, tools, evals)

- **Schema vs Chat Completions:** Responses uses `text.format`; Chat Completions uses `response_format`. Mixing them is a common 400.
- **`arguments` is a JSON string:** `json.loads(item.arguments)` before indexing. `item.arguments["query"]` raises `TypeError`.
- **Tool loop repeats:** pair `function_call_output` with the model's `call_id`. Cap steps (`MAX_TOOL_STEPS`). Keep `LLM_PROVIDER=fake` for graded work.
- **Invalid tool args in CI:** that is supposed to fail validation (`strict=True`). Do not coerce `query: 1` into `"1"`.
- **Eval wants a key:** unset `LLM_PROVIDER` or set it to `fake`. Live pass rates are reported with no threshold claimed and are not a CI gate.
- **Refusal vs ValidationError:** `response.refusal` is not malformed JSON. Do not retry-parse it as an Incident.

## Module 4 (embeddings, RAG, numpy)

- **numpy wheels, not source builds:** `uv sync --locked` should download a wheel for CPython 3.11–3.13 on Windows amd64, macOS x86_64 **and arm64**, and manylinux. If uv starts compiling numpy, the interpreter architecture is wrong.
- **Apple Silicon:** `python -c "import platform; print(platform.machine())"` should print `arm64`. A Rosetta (x86_64) Python cannot import an arm64 wheel ("Bad CPU type"). Install native uv/CPython, then `uv sync --locked`.
- **Windows ARM64:** use a numpy wheel if uv offers one. Do not install Visual Studio just to compile numpy for this course. WSL2 (x86_64 or arm64 Linux wheels) is the fallback.
- **Graded embeddings are fake:** `FakeEmbedder` is a hashing trick. Precomputed vectors: `data/embeddings/payments-api.json`. Rebuild: `uv run python scripts/build_embedding_fixtures.py`.
- **Wrong API:** live embeddings → `client.embeddings.create`. Live generation in RAG → `client.responses.create`. Never Assistants, never Assistants file_search in CI.
- **Eval command:** `uv run docsdesk eval` (or `uv run python -m docsdesk eval`). Keep `LLM_PROVIDER=fake`. A red recall@5 is a chunker/index bug, not a missing key.

## Module 5 (agents, triage, MCP)

- **Trajectory stuck on turn 1:** reuse one `FakeLLM` instance. `trajectories=` advances one scripted turn per `complete()`. A new FakeLLM restarts at turn 0.
- **Cap never fires:** the script must keep returning `tools`. A `message` turn stops with `done`. Runaway fixture: `keep calling tools forever`.
- **`propose_page` still runs:** set both `run_agent_loop(..., approve=False)` and `ToolRunner.approved = False`. The gate is simulated (`would_write`); nothing is written or emailed.
- **Agent eval:** `uv run docsdesk eval-agent` (or `uv run python -m docsdesk eval-agent`). Keep `LLM_PROVIDER=fake`. Failures are loop/cap/approval bugs, not a missing key.
- **Framework lesson (5.5):** do not `uv add openai-agents` or LangChain. The facade is `course_kit.agent.facade`.
- **MCP lesson (5.6):** in-process JSON-RPC only. No stdio server in CI. Hosted remote MCP is optional and paid.
- **Wrong API:** live generation still uses `client.responses.create`. Never Assistants.

## Module 6 (evals, observability, production)

- **CI gate red on fake:** keep `LLM_PROVIDER=fake`. An injected regression (wrong `expected_answer`) is *supposed* to fail the gate. Do not "fix" it with a live key.
- **Judge vs golden:** exact match is for FakeLLM fixtures. An LLM-as-judge needs calibration (`agreement_rate`) before it is a gate. Live judges report a rate; this course claims no threshold.
- **Request id vs response id:** `LLMResponse.id` is `resp_…`. `LLMResponse.request_id` is the HTTP id (OpenAI Python SDK `_request_id`). Log both if you need them; quote `request_id` in support tickets.
- **Port 8000:** FastAPI tests use TestClient (no port). Optional local uvicorn: `--host 127.0.0.1`. Windows: `netstat -ano | findstr :8000`. macOS/Linux: `lsof -i :8000`. Then `--port 8001`.
- **Docker:** optional. Windows/macOS need Docker Desktop running. Linux needs permission for the daemon (`docker` group). CI never `docker build`. Never bake `OPENAI_API_KEY` into an image. `.env` is in `deploy/.dockerignore`.
- **FastAPI extra:** `uv sync --locked --group prod`. Without it, `tests/test_docsdesk_service.py` skips. Concept 6.6 exercises still grade.
- **Env vars:** Windows `set LLM_PROVIDER=fake`. PowerShell `$env:LLM_PROVIDER="fake"`. macOS/Linux `export LLM_PROVIDER=fake`.
- **Wrong API:** live generation still uses `client.responses.create`. Never Assistants.

## Still stuck?

1. Paste `uv run python scripts/doctor.py --offline` into a [bug issue](../../.github/ISSUE_TEMPLATE/bug.yml) (no keys).
2. Include OS, `uv run python --version`, and the exact command that failed.
3. Check [guide 05](../../guides/05_uv_and_debugging.md) for import/kernel mistakes that are not install problems.
