"""Check that this machine can run the core course.

Java analogy: this is a local health check, like hitting an app's /ready endpoint
before you start a debugging session. It does not change data, send email, or
call a paid API.

Usage (from the repository root):

    uv run python scripts/doctor.py
    uv run python scripts/doctor.py --offline
"""

from __future__ import annotations

import argparse
import os
import platform
import shutil
import sys
import urllib.error
import urllib.request
from collections.abc import Callable
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIN_VERSION = (3, 11)


def is_wsl() -> bool:
    if platform.system() != "Linux":
        return False
    try:
        text = Path("/proc/version").read_text(encoding="utf-8").lower()
    except OSError:
        return False
    return "microsoft" in text or "wsl" in text


def _ok(message: str) -> tuple[str, str]:
    return "ok", message


def _warn(message: str) -> tuple[str, str]:
    return "warn", message


def _fail(message: str) -> tuple[str, str]:
    return "fail", message


def check_python() -> tuple[str, str]:
    version = sys.version_info
    current = f"{version.major}.{version.minor}.{version.micro}"
    if (version.major, version.minor) < MIN_VERSION:
        return _fail(f"Python {current} is too old; this course needs 3.11+")
    return _ok(f"Python {current} ({sys.executable})")


def check_repo_root() -> tuple[str, str]:
    if not (ROOT / "pyproject.toml").is_file():
        return _fail(f"pyproject.toml not found at {ROOT}")
    return _ok(f"Repository root {ROOT}")


def check_venv() -> tuple[str, str]:
    in_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
    venv_dir = ROOT / ".venv"
    if in_venv:
        return _ok(f"Virtual environment active ({sys.prefix})")
    if venv_dir.is_dir():
        return _warn(
            "`.venv` exists but this interpreter is not inside it. "
            "In Cursor/VS Code: Python: Select Interpreter → `.venv`."
        )
    return _fail("No `.venv`. From the repo root run: uv sync --locked --group dev")


def check_uv() -> tuple[str, str]:
    path = shutil.which("uv")
    if path:
        return _ok(f"uv on PATH ({path})")
    return _warn(
        "`uv` is not on PATH. Install it, then restart the terminal. "
        "See docs/setup/troubleshooting.md"
    )


def check_import(
    module: str, *, required: bool, hint: str, need_attr: str | None = None
) -> tuple[str, str]:
    try:
        imported = __import__(module)
    except ImportError:
        if required:
            return _fail(f"Cannot import {module}. {hint}")
        return _warn(f"{module} not installed ({hint})")
    if need_attr and not hasattr(imported, need_attr):
        if required:
            return _fail(f"{module} is incomplete (missing {need_attr}). {hint}")
        return _warn(f"{module} is not fully installed ({hint})")
    return _ok(f"import {module}")


def check_pypi() -> tuple[str, str]:
    request = urllib.request.Request("https://pypi.org/simple/", method="HEAD")
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            status = getattr(response, "status", 200)
            if status >= 400:
                return _warn(f"PyPI responded with HTTP {status} (proxy, SSL, or VPN?)")
            return _ok("PyPI is reachable")
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return _warn(f"Cannot reach pypi.org ({exc}). Check proxy, SSL inspection, or VPN.")


def collect_hints() -> list[str]:
    hints: list[str] = []
    system = platform.system()
    machine = platform.machine()

    if system == "Windows":
        hints.append(
            "Windows: if `python` is not found, try `py -3.12` or `uv python install 3.12`."
        )
        hints.append("Windows long paths: `git config --global core.longpaths true`.")
        if "WindowsApps" in sys.executable:
            hints.append(
                "This looks like the Microsoft Store Python stub. Use uv's interpreter instead."
            )
    elif system == "Darwin":
        hints.append("macOS: `python3` is the usual command; `python` may be missing.")
        if machine.lower() in {"arm64", "aarch64"}:
            hints.append(
                "Apple Silicon: use an arm64 uv/Python build. "
                "'Bad CPU type in executable' means a Rosetta/x86_64 binary. "
                "numpy must be the arm64 wheel (Module 4)."
            )
    else:
        hints.append("Linux: `python3` is the usual command; install uv, then `uv sync --locked`.")

    if is_wsl():
        hints.append(
            "WSL: run the course inside Linux (this shell), not mixed with Windows Python paths."
        )

    proxy_names = [
        name
        for name in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy")
        if os.environ.get(name)
    ]
    if proxy_names:
        hints.append(
            "Proxy variables are set ("
            + ", ".join(proxy_names)
            + "). uv uses them. For SSL inspection, point SSL_CERT_FILE at your corporate CA."
        )
    if os.environ.get("SSL_CERT_FILE") or os.environ.get("REQUESTS_CA_BUNDLE"):
        hints.append("Custom TLS bundle detected (SSL_CERT_FILE or REQUESTS_CA_BUNDLE).")

    if shutil.which("python") is None and shutil.which("python3") is not None:
        hints.append("`python` is not on PATH; `python3` is. Prefer `uv run python`.")

    hints.append(
        "Jupyter kernel: Python: Select Interpreter → `.venv`, then pick that kernel in the notebook."
    )
    hints.append("FAQ: docs/setup/faq.md. More detail: docs/setup/troubleshooting.md")
    return hints


def run_checks(*, offline: bool) -> list[tuple[str, str]]:
    checks: list[Callable[[], tuple[str, str]]] = [
        check_python,
        check_repo_root,
        check_venv,
        check_uv,
        lambda: check_import(
            "pydantic",
            required=True,
            hint="uv sync --locked --group dev",
        ),
        lambda: check_import(
            "mini_agent",
            required=True,
            hint="run doctor from the repo root after uv sync --locked --group dev",
        ),
        lambda: check_import(
            "course_kit",
            required=True,
            hint="run doctor from the repo root after uv sync --locked --group dev",
        ),
        lambda: check_import(
            "docsdesk",
            required=True,
            hint="run doctor from the repo root after uv sync --locked --group dev",
        ),
        lambda: check_import(
            "httpx",
            required=True,
            hint="uv sync --locked --group dev",
        ),
        lambda: check_import(
            "numpy",
            required=True,
            hint="uv sync --locked --group dev (numpy wheel; see docs/setup/troubleshooting.md)",
        ),
        lambda: check_import(
            "ipykernel",
            required=False,
            hint="needed for notebooks: uv sync --locked --group dev",
        ),
        lambda: check_import(
            "gradio",
            required=False,
            hint="optional demo: uv sync --locked --group dev --group demo",
            need_attr="Blocks",
        ),
    ]
    results = [check() for check in checks]
    if not offline:
        results.append(check_pypi())
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Course environment health check")
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Skip the PyPI connectivity probe (proxy/SSL/VPN hint).",
    )
    args = parser.parse_args(argv)

    print("Python for Java AI Engineers — doctor")
    print("=" * 40)
    print(f"OS: {platform.system()} {platform.release()} ({platform.machine()})")
    if is_wsl():
        print("Environment: WSL")
    print(f"Python: {sys.version.split()[0]}")
    key_set = bool(os.environ.get("OPENAI_API_KEY"))
    print(f"OPENAI_API_KEY set: {key_set} (value not printed)")
    print()

    results = run_checks(offline=args.offline)
    failed = 0
    for status, message in results:
        if status == "ok":
            prefix = "OK  "
        elif status == "warn":
            prefix = "WARN"
        else:
            prefix = "FAIL"
            failed += 1
        print(f"{prefix}  {message}")

    print()
    print("Hints")
    print("-----")
    for hint in collect_hints():
        print(f"- {hint}")

    print()
    if failed:
        print("Result: not ready. Fix the FAIL lines, then re-run doctor.")
        return 1
    print("Result: ready for Modules 0A–7, Electives (A), and the core notebooks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
