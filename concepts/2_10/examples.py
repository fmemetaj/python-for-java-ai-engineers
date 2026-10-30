"""Load the versioned DocsDesk prompt and grade a fake eval case."""

from __future__ import annotations

from docsdesk.session import PROMPT_VERSION, load_instructions

text = load_instructions()
assert "DocsDesk" in text
assert "email" in text.lower()
assert PROMPT_VERSION == "answer_from_doc.v1"
print("2.10 examples ok")
