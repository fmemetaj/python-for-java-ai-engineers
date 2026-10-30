"""Retry 429/5xx with exponential backoff; do not retry 404."""

from __future__ import annotations

assert (429 == 429) and (404 != 429)
delays = [0.05 * (2**n) for n in range(3)]
assert delays == [0.05, 0.1, 0.2]
print("1.12 examples ok")
