"""Every relative Markdown link in the repo must resolve to a file."""

from __future__ import annotations

import importlib.util

from course_kit.loader import repo_root


def _load_checker():
    path = repo_root() / "scripts" / "check_markdown_links.py"
    spec = importlib.util.spec_from_file_location("check_markdown_links", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


checker = _load_checker()


def test_repo_relative_markdown_links_resolve() -> None:
    issues = checker.broken_links(repo_root())
    rendered = "\n".join(
        f"{source.relative_to(repo_root())} -> {href}" for source, href, _dest in issues
    )
    assert issues == [], rendered


def test_checker_parses_standard_links() -> None:
    found = checker.targets(
        "See [Module 0A](modules/0a-fundamentals/README.md) and https://example.com."
    )
    assert found == ["modules/0a-fundamentals/README.md"]


def test_checker_finds_markdown_files() -> None:
    files = checker.markdown_files(repo_root())
    assert any(path.name == "README.md" and path.parent == repo_root() for path in files)
