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

## Still stuck?

1. Paste `uv run python scripts/doctor.py --offline` into a [bug issue](../../.github/ISSUE_TEMPLATE/bug.yml) (no keys).
2. Include OS, `uv run python --version`, and the exact command that failed.
3. Check [guide 05](../../guides/05_uv_and_debugging.md) for import/kernel mistakes that are not install problems.
