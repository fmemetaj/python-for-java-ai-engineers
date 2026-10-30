"""asyncio overlaps waits on one thread; it is not a thread pool."""

from __future__ import annotations

import asyncio


async def fake_lookup(name: str) -> str:
    await asyncio.sleep(0)
    return name


async def main() -> None:
    names = await asyncio.gather(fake_lookup("a"), fake_lookup("b"))
    assert names == ["a", "b"]


asyncio.run(main())
print("0.29 examples ok")
