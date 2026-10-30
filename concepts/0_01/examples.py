"""Runnable examples for 0.1 — running scripts vs importing them."""

from __future__ import annotations


def run_mode(module_name: str) -> str:
    return "script" if module_name == "__main__" else "imported"


def banner(module_name: str, script_name: str) -> str:
    return f"{script_name}: {run_mode(module_name)}"


assert run_mode("__main__") == "script"
assert run_mode("concepts.demo") == "imported"
assert banner("__main__", "log_stats.py") == "log_stats.py: script"
assert banner("fundamentals.log_stats", "log_stats.py") == "log_stats.py: imported"


def main() -> None:
    print(banner(__name__, "examples.py"))
    print("0.1 examples ok")


if __name__ == "__main__":
    main()
