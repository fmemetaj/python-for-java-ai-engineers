"""Course tokenizer — a stand-in for billed tokens, not tiktoken.

Real OpenAI tokenization is a learned BPE split (not words, not characters).
Graded exercises stay deterministic and offline, so we use a fixed rule:
four characters ≈ one token, matching the FakeLLM usage helper.
https://help.openai.com/en/articles/4936856-understanding-and-counting-tokens
"""

from __future__ import annotations


def estimate_tokens(text: str) -> int:
    """Return a positive token count using the course 4-characters ≈ 1 token rule."""
    if not text:
        return 0
    return max(1, (len(text) + 3) // 4)


def whitespace_tokens(text: str) -> list[str]:
    """Split on whitespace. Useful as a *wrong* mental model next to estimate_tokens."""
    return [part for part in text.split() if part]
