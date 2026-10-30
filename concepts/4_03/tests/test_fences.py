from course_kit.loader import load_concept_module

fences = load_concept_module("4_03", "fences")

DOC = """# Title

intro

```java
@RestController
public class PaymentController {
    @PostMapping
    public void create() {}
}
```

outro
"""


def test_fence_is_one_code_chunk() -> None:
    chunks = fences.chunk_preserving_fences(DOC, max_chars=24, path="PaymentController.md")
    code = [c for c in chunks if c.is_code]
    assert len(code) == 1
    assert "@PostMapping" in code[0].text
    assert code[0].text.strip().startswith("```")
    assert code[0].text.strip().endswith("```")


def test_prose_still_chunked() -> None:
    chunks = fences.chunk_preserving_fences(DOC, max_chars=24, path="PaymentController.md")
    prose = [c for c in chunks if not c.is_code]
    assert prose
    assert any("intro" in c.text or "Title" in c.text for c in prose)
