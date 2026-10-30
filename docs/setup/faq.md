# FAQ — setup on Windows, macOS, and Linux

Short answers for the problems `scripts/doctor.py` and new learners hit first. Longer versions: [troubleshooting.md](troubleshooting.md). Official uv install: [astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/).

## Start here (all OS)

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/).
2. From the repository root: `uv python install 3.12`
3. `uv sync --locked --group dev`
4. `uv run python scripts/doctor.py --offline`
5. Open [Module 0A · concept 0.1](../../concepts/0_01/README.md) (or the [placement check](../../placement/README.md) if you already know some Python).

Prefer `uv run python` over a system `python`. Select this repo's `.venv` in the editor.

## Windows

**`python` opens the Microsoft Store.** Use `py -3.12` or `uv run python`. The Store stub is not an interpreter — doctor warns if it sees `WindowsApps` on PATH.

**`uv` is not recognized after install.** It usually lands in `%USERPROFILE%\.local\bin`. Add that directory in Settings → Environment variables, then restart **both** the terminal and the editor (Cursor/VS Code inherit PATH at launch).

**Clone or `uv sync` fails on long paths.** `git config --global core.longpaths true`.

**Jupyter kernel missing.** Command Palette → Python: Select Interpreter → `.venv\Scripts\python.exe`. If the notebook opens as JSON: Open With → Jupyter Notebook.

**`LLM_PROVIDER`.** `cmd`: `set LLM_PROVIDER=fake`. PowerShell: `$env:LLM_PROVIDER="fake"`.

**Encoding / mojibake in `cmd.exe`.** Use Windows Terminal. CI sets `PYTHONUTF8=1`.

**WSL.** Do the entire course inside Linux: clone, uv, `.venv`, notebooks. Do not mix a Windows venv with `/home/...` paths.

## macOS

**`python` not found.** That is normal. Use `python3` or `uv run python`.

**`uv` not found.** Installer PATH is `~/.local/bin`. Restart the terminal or `source ~/.local/bin/env`.

**Apple Silicon "Bad CPU type in executable".** The shell is running an x86_64 (Rosetta) binary. Open a native Terminal.app (or `arch -arm64 zsh`), reinstall uv, `uv python install 3.12`, then `uv sync --locked`. `python -c "import platform; print(platform.machine())"` should print `arm64`.

**Jupyter kernel.** Python: Select Interpreter → `.venv/bin/python`.

**`LLM_PROVIDER`.** `export LLM_PROVIDER=fake`.

## Linux

**`python` not found.** Use `python3` or `uv run python`. Do not install an outdated distro `uv` package; use the [official script](https://docs.astral.sh/uv/getting-started/installation/).

**`uv` not found.** Same as macOS: `~/.local/bin` plus a new shell.

**numpy / wheels compiling from source.** On x86_64 and aarch64 CPython 3.11–3.13, `uv sync --locked` should download a wheel. A source build usually means the interpreter architecture is wrong.

**Docker (optional Module 6).** Your user needs permission for the daemon (`docker` group). CI never `docker build`.

**`LLM_PROVIDER`.** `export LLM_PROVIDER=fake`.

## All platforms

**Need a paid API key?** No. Graded work uses `LLM_PROVIDER=fake`.

**`.env`.** Copy `.env.example` → `.env` for local overrides. Never commit `.env`. Doctor reports whether `OPENAI_API_KEY` is set, not the value.

**Which API?** `client.responses.create` only. The Assistants API was sunset 2026-08-26 and is out of scope.

**Proxy / SSL / VPN.** uv honors `HTTPS_PROXY`. Corporate TLS inspection needs `SSL_CERT_FILE` pointed at your CA. Do not disable verification. A VPN can block PyPI — run doctor without `--offline` to probe `https://pypi.org/simple/`.

**Gradio tests skipped.** Default `uv sync --locked --group dev` does not install Gradio. That is expected. Optional: `--group demo`.

**Still stuck?** Paste `uv run python scripts/doctor.py --offline` into a [bug issue](../../.github/ISSUE_TEMPLATE/bug.yml) (no keys), with OS and `uv run python --version`.
