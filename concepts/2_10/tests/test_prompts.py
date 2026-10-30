from pathlib import Path

from course_kit.loader import load_concept_module, repo_root

prompts = load_concept_module("2_10", "prompts")


def test_load_and_version() -> None:
    path = repo_root() / "src" / "docsdesk" / "prompts" / "answer_from_doc.v1.txt"
    text = prompts.load_prompt(path)
    assert "DocsDesk" in text
    assert prompts.prompt_version(path) == "answer_from_doc.v1"
    assert prompts.prompt_version(Path("tmp/foo.v2.txt")) == "foo.v2"
