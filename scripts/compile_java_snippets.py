"""Compile every Java snippet shipped with Module 0A (JDK 21).

Each file is compiled on its own so public class names only need to
match the file name, not be unique across the course.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def java_files() -> list[Path]:
    return sorted((ROOT / "concepts").glob("*/java/*.java"))


def compile_all(*, javac: str) -> int:
    files = java_files()
    if not files:
        print("No Java snippets found under concepts/*/java/")
        return 1
    failed = 0
    with tempfile.TemporaryDirectory(prefix="course-java-") as tmp:
        out = Path(tmp)
        for path in files:
            command = [
                javac,
                "-encoding",
                "UTF-8",
                "-source",
                "21",
                "-d",
                str(out / path.stem),
                str(path),
            ]
            result = subprocess.run(command, check=False, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"OK   {path.relative_to(ROOT)}")
            else:
                failed += 1
                print(f"FAIL {path.relative_to(ROOT)}")
                print(result.stderr or result.stdout)
    if failed:
        print(f"{failed} Java snippet(s) failed to compile")
        return 1
    print(f"{len(files)} Java snippet(s) compiled")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compile Module 0A Java snippets")
    parser.add_argument("--javac", default=shutil.which("javac") or "javac")
    args = parser.parse_args(argv)
    if shutil.which(args.javac) is None and not Path(args.javac).is_file():
        print("javac not found. Install JDK 21 or skip this script locally.")
        return 2
    return compile_all(javac=args.javac)


if __name__ == "__main__":
    raise SystemExit(main())
