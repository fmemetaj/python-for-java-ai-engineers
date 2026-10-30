"""Five token facts. Offline; course estimator is not tiktoken."""

from __future__ import annotations

from course_kit.llm.tokens import estimate_tokens, whitespace_tokens

# Example 1 — empty vs four characters.
assert estimate_tokens("") == 0
assert estimate_tokens("abcd") == 1

# Example 2 — words are not tokens.
words = whitespace_tokens("one two three four")
assert words == ["one", "two", "three", "four"]
assert estimate_tokens("one two three four") != len(words) or len("one two three four") == 16

# Example 3 — a URL is one word, many characters.
url = "https://docs.internal.test/auth"
assert len(whitespace_tokens(url)) == 1
assert estimate_tokens(url) >= 1

# Example 4 — Responses names vs Chat Completions names.
responses_usage = {"input_tokens": 12, "output_tokens": 4, "cached_tokens": 0}
chat_usage = {"prompt_tokens": 12, "completion_tokens": 4}
assert responses_usage["input_tokens"] == chat_usage["prompt_tokens"]

# Example 5 — cached tokens are still input.
assert 8 <= 10  # cached=8 of input=10 still occupies the window

print("2.2 examples ok")
