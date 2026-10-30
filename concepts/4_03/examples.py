"""Size vs structure-aware chunking. Offline; no embeddings required."""

from __future__ import annotations

from course_kit.rag.chunking import chunk_by_size, chunk_preserving_fences, chunk_structured

text = "# Title\n\nProse about refunds.\n\n```java\nclass A { void f() {} }\n```\n\nMore prose.\n"

# Example 1 — size windows exist.
sized = chunk_by_size(text, max_chars=40, overlap=8, path="demo.md")
assert sized[0].chunk_id.startswith("demo:")

# Example 2 — tiny windows can split a fence.
tiny = chunk_by_size(text, max_chars=20, overlap=0, path="demo.md")
fence_bits = [c for c in tiny if "```" in c.text]
assert len(fence_bits) >= 1

# Example 3 — preserving fences keeps one code chunk.
kept = chunk_preserving_fences(text, max_chars=40, overlap=8, path="demo.md")
code = [c for c in kept if c.is_code]
assert len(code) == 1
assert "class A" in code[0].text
assert code[0].text.count("```") == 2

# Example 4 — structured chunks know the heading.
structured = chunk_structured("# Refunds\n\nPartial refunds are allowed.\n", path="refunds.md")
assert any(c.heading == "Refunds" for c in structured)

# Example 5 — ids use the file stem.
assert structured[0].chunk_id.startswith("refunds:")

print("4.3 examples ok")
