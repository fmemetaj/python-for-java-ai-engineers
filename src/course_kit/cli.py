"""Command-line checkpoint: `uv run course check m0a|m0b|m1|m2|m3`."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

from .catalog import (
    CONCEPTS_0A,
    CONCEPTS_0B,
    CONCEPTS_1,
    CONCEPTS_2,
    CONCEPTS_3,
    MODULE_0A,
    MODULE_0B,
    MODULE_1,
    MODULE_2,
    MODULE_3,
    Concept,
)
from .loader import repo_root


def _run_pytest(paths: list[Path], *, impl: str) -> int:
    env = os.environ.copy()
    env["COURSE_IMPL"] = impl
    command = [sys.executable, "-m", "pytest", "-q", "--tb=line", *[str(p) for p in paths]]
    result = subprocess.run(command, cwd=repo_root(), env=env, check=False)
    return result.returncode


def _label(passed: bool) -> str:
    return "pass" if passed else "fail"


def _grade_concepts(concepts: Sequence[Concept], *, impl: str) -> int:
    root = repo_root()
    failed = 0
    for concept in concepts:
        folder = concept["folder"]
        skip_path = root / "concepts" / folder / "tests" / "test_skip.py"
        exercise_paths = sorted(
            path
            for path in (root / "concepts" / folder / "tests").glob("test_*.py")
            if path.name != "test_skip.py"
        )
        skip_ok = _run_pytest([skip_path], impl=impl) == 0
        exercise_ok = _run_pytest(exercise_paths, impl=impl) == 0 if exercise_paths else True
        if not skip_ok or not exercise_ok:
            failed += 1
        kind = "NEW" if concept["kind"] == "new" else "Analog"
        print(
            f"{concept['id']:<6} {concept['title'][:42]:<42} "
            f"{kind:<6} skip={_label(skip_ok)}  exercise={_label(exercise_ok)}"
        )
    return failed


def check_m0a(*, impl: str) -> int:
    root = repo_root()
    print(f"{MODULE_0A['title']}")
    print(f"cost: {MODULE_0A['cost']} | COURSE_IMPL={impl} | offline")
    print()

    failed = _grade_concepts(CONCEPTS_0A, impl=impl)
    log_ok = _run_pytest([root / "fundamentals" / "test_log_stats.py"], impl=impl) == 0
    place_ok = _run_pytest([root / "placement" / "test_self_check.py"], impl=impl) == 0
    if not log_ok:
        failed += 1
    if not place_ok:
        failed += 1
    print()
    print(f"log_stats   {_label(log_ok)}")
    print(f"placement   {_label(place_ok)}")
    print()
    total = len(CONCEPTS_0A) + 2
    passed = total - failed
    print(f"{passed}/{total} checks passed")
    if impl == "exercises":
        print("Fill concepts/<id>/exercises/*.py, then re-run. Solutions stay in solutions/.")
    return 0 if failed == 0 else 1


def check_m0b(*, impl: str) -> int:
    root = repo_root()
    print(f"{MODULE_0B['title']}")
    print(f"cost: {MODULE_0B['cost']} | COURSE_IMPL={impl} | offline")
    print()

    failed = _grade_concepts(CONCEPTS_0B, impl=impl)
    registry_ok = _run_pytest([root / "fundamentals" / "test_tool_registry.py"], impl=impl) == 0
    if not registry_ok:
        failed += 1
    print()
    print(f"tool_registry   {_label(registry_ok)}")
    print()
    total = len(CONCEPTS_0B) + 1
    passed = total - failed
    print(f"{passed}/{total} checks passed")
    if impl == "exercises":
        print("Fill concepts/<id>/exercises/*.py, then re-run. Solutions stay in solutions/.")
    return 0 if failed == 0 else 1


def check_m1(*, impl: str) -> int:
    root = repo_root()
    print(f"{MODULE_1['title']}")
    print(f"cost: {MODULE_1['cost']} | COURSE_IMPL={impl} | offline")
    print()

    failed = _grade_concepts(CONCEPTS_1, impl=impl)
    docs_ok = _run_pytest([root / "tests" / "test_docsdesk.py"], impl=impl) == 0
    llm_ok = _run_pytest([root / "tests" / "test_fake_llm.py"], impl=impl) == 0
    if not docs_ok:
        failed += 1
    if not llm_ok:
        failed += 1
    print()
    print(f"docsdesk    {_label(docs_ok)}")
    print(f"fake_llm    {_label(llm_ok)}")
    print()
    total = len(CONCEPTS_1) + 2
    passed = total - failed
    print(f"{passed}/{total} checks passed")
    if impl == "exercises":
        print("Fill concepts/<id>/exercises/*.py, then re-run. Solutions stay in solutions/.")
    return 0 if failed == 0 else 1


def check_m2(*, impl: str) -> int:
    root = repo_root()
    print(f"{MODULE_2['title']}")
    print(f"cost: {MODULE_2['cost']} | COURSE_IMPL={impl} | offline")
    print()

    failed = _grade_concepts(CONCEPTS_2, impl=impl)
    docs_ok = _run_pytest([root / "tests" / "test_docsdesk.py"], impl=impl) == 0
    llm_ok = _run_pytest([root / "tests" / "test_fake_llm.py"], impl=impl) == 0
    cost_ok = _run_pytest([root / "tests" / "test_cost.py"], impl=impl) == 0
    if not docs_ok:
        failed += 1
    if not llm_ok:
        failed += 1
    if not cost_ok:
        failed += 1
    print()
    print(f"docsdesk    {_label(docs_ok)}")
    print(f"fake_llm    {_label(llm_ok)}")
    print(f"cost        {_label(cost_ok)}")
    print()
    total = len(CONCEPTS_2) + 3
    passed = total - failed
    print(f"{passed}/{total} checks passed")
    if impl == "exercises":
        print("Fill concepts/<id>/exercises/*.py, then re-run. Solutions stay in solutions/.")
    return 0 if failed == 0 else 1


def check_m3(*, impl: str) -> int:
    root = repo_root()
    print(f"{MODULE_3['title']}")
    print(f"cost: {MODULE_3['cost']} | COURSE_IMPL={impl} | offline")
    print()

    failed = _grade_concepts(CONCEPTS_3, impl=impl)
    docs_ok = _run_pytest([root / "tests" / "test_docsdesk.py"], impl=impl) == 0
    llm_ok = _run_pytest([root / "tests" / "test_fake_llm.py"], impl=impl) == 0
    eval_ok = _run_pytest([root / "tests" / "test_docsdesk_eval.py"], impl=impl) == 0
    if not docs_ok:
        failed += 1
    if not llm_ok:
        failed += 1
    if not eval_ok:
        failed += 1
    print()
    print(f"docsdesk    {_label(docs_ok)}")
    print(f"fake_llm    {_label(llm_ok)}")
    print(f"evals       {_label(eval_ok)}")
    print()
    total = len(CONCEPTS_3) + 3
    passed = total - failed
    print(f"{passed}/{total} checks passed")
    if impl == "exercises":
        print("Fill concepts/<id>/exercises/*.py, then re-run. Solutions stay in solutions/.")
    return 0 if failed == 0 else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Course checkpoints")
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="Run a module checkpoint")
    check.add_argument("module", choices=["m0a", "m0b", "m1", "m2", "m3"], help="Module id")
    check.add_argument(
        "--solutions",
        action="store_true",
        help="Grade the committed solutions instead of learner files",
    )
    args = parser.parse_args(argv)
    impl = "solutions" if args.solutions else os.environ.get("COURSE_IMPL", "exercises")
    if args.module == "m0a":
        return check_m0a(impl=impl)
    if args.module == "m0b":
        return check_m0b(impl=impl)
    if args.module == "m1":
        return check_m1(impl=impl)
    if args.module == "m2":
        return check_m2(impl=impl)
    if args.module == "m3":
        return check_m3(impl=impl)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
