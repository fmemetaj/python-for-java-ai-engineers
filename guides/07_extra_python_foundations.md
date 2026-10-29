# 07 — Further Python foundations (read only when useful)

This is a **supplemental reference**, not a mandatory lesson. The seven notebooks remain a focused bridge for experienced Java developers. Some topics from [Ed Donner's companion guides](https://github.com/ed-donner/llm_engineering/tree/main/guides) are intentionally summarized or deferred.

## Imports, modules and package boundaries

Think of Python modules like individual Java source files with directly importable definitions, and Python packages like namespaces. `import json` makes the **module** available; `from pathlib import Path` imports a **name** directly.

```python
import json
from pathlib import Path
payload = json.loads('{"priority": "high"}')
file_name = Path("example.json").name
```

Avoid naming your own files `json.py` or `asyncio.py`, which can shadow standard-library packages.

## String slices, formatting and date formatting

```python
from datetime import datetime, timezone
subject = "  reset password  "
print(subject.strip()[:5])
print(" ".join(subject.split()))
print(f"Ticket {7:03d} created {datetime.now(timezone.utc):%Y-%m-%d}")
```

Python slicing excludes the end index; f-string format specifiers handle numbers and dates concisely.

## Files, paths, globbing and JSON

```python
from pathlib import Path
import json
from tempfile import TemporaryDirectory
with TemporaryDirectory() as folder:
    path = Path(folder) / "tickets.json"
    path.write_text(json.dumps([{"id": 1}]), encoding="utf-8")
    assert json.loads(path.read_text(encoding="utf-8"))[0]["id"] == 1
    print(list(Path(folder).glob("*.json")))
```

**Serialization security:** only unpickle trusted bytes; `pickle.load()` can execute malicious code. Use JSON for untrusted structured data and validate its contents with Pydantic.

## Class methods and inheritance

Python's `@classmethod` takes `cls` rather than an instance `self`. Inheritance uses `class Child(Parent):`. These concepts are familiar from Java; add them only when reading a library that uses them.

## Docker (optional, familiar to many Java engineers)

A Python image can be started with `docker run --rm python:3.12 python -c "print(2+2)"`. For a real service, prefer pinned images, least privileges, vulnerability scans and reproducible dependency installation. The course uses `uv` without Docker because the beginner learning environment should be lightweight.

## Environment variables and API clients

```python
import os
api_key = os.environ.get("MY_API_KEY")  # returns None when unset
```

Never commit keys or print them in notebooks. A CLI API call uses an SDK or HTTP endpoint; this is separate from any ChatGPT subscription. The optional Ollama demo uses a **localhost-only** HTTP endpoint instead of a paid API.

## Debugging NameError and kernel state

A notebook retains variables until you restart its kernel. `NameError` may simply mean you executed cells out of order. Restart and **Run All**, then check imports and local variable spelling.

**Recommended reading:** [Ed Donner's foundations](https://github.com/ed-donner/llm_engineering/blob/main/guides/06_python_foundations.ipynb), [intermediate Python](https://github.com/ed-donner/llm_engineering/blob/main/guides/10_intermediate_python.ipynb), [async Python](https://github.com/ed-donner/llm_engineering/blob/main/guides/11_async_python.ipynb) and [technical foundations](https://github.com/ed-donner/llm_engineering/blob/main/guides/04_technical_foundations.ipynb). This is independent, original course material; no endorsement is implied.

[Back to guides index](README.md).
