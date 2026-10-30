"""Provider switch: fake default, live opt-in."""

from __future__ import annotations

import pytest

from course_kit.llm import FakeLLM, get_client

assert isinstance(get_client("fake"), FakeLLM)
with pytest.raises(RuntimeError, match="responses.create"):
    get_client("openai")
with pytest.raises(ValueError):
    get_client("assistants")
print("2.5 examples ok")
