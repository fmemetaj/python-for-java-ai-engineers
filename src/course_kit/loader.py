"""Load a learner exercise or the matching solution.

Set COURSE_IMPL=exercises (default) or COURSE_IMPL=solutions.
Java analogy: this is a test profile switch, like @ActiveProfiles("solutions").
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path
from types import ModuleType

VALID_IMPL = {"exercises", "solutions"}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def impl_name() -> str:
    value = os.environ.get("COURSE_IMPL", "exercises")
    if value not in VALID_IMPL:
        expected = " or ".join(sorted(VALID_IMPL))
        raise ValueError(f"COURSE_IMPL must be {expected}, got {value!r}")
    return value


def _safe_part(value: str) -> str:
    """Allow only lesson file names (no path separators or traversal)."""
    if not value or any(ch in value for ch in ("/", "\\", ".", "\x00")):
        raise ValueError(f"invalid path part: {value!r}")
    if not value.replace("_", "").isalnum():
        raise ValueError(f"invalid path part: {value!r}")
    return value


def _load(path: Path, module_name: str) -> ModuleType:
    if not path.is_file():
        raise FileNotFoundError(path)
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def load_concept_module(folder: str, name: str) -> ModuleType:
    """Load concepts/<folder>/<impl>/<name>.py."""
    impl = impl_name()
    path = repo_root() / "concepts" / _safe_part(folder) / impl / f"{_safe_part(name)}.py"
    return _load(path, f"course_{folder}_{impl}_{name}")


def load_fundamentals() -> ModuleType:
    """Load the Module 0A deliverable `fundamentals/log_stats.py`."""
    root = repo_root()
    if impl_name() == "solutions":
        path = root / "fundamentals" / "solutions" / "log_stats.py"
    else:
        path = root / "fundamentals" / "log_stats.py"
    return _load(path, f"course_fundamentals_{impl_name()}")


def load_placement() -> ModuleType:
    """Load placement/self_check.py (or its solution)."""
    root = repo_root()
    if impl_name() == "solutions":
        path = root / "placement" / "solutions" / "self_check.py"
    else:
        path = root / "placement" / "self_check.py"
    return _load(path, f"course_placement_{impl_name()}")
