from course_kit.loader import load_concept_module

proto = load_concept_module("0_22", "protocol")


class ExtraRetriever:
    def search(self, query: str) -> list[str]:
        return [f"extra:{query}"]


def test_memory_search() -> None:
    memory = proto.MemoryRetriever(["login timeout", "invoice missing", "login ok"])
    assert memory.search("login") == ["login timeout", "login ok"]
    assert proto.top_hit(memory, "invoice") == "invoice missing"
    assert proto.top_hit(memory, "absent") is None


def test_structural_other_class() -> None:
    assert proto.top_hit(ExtraRetriever(), "disk") == "extra:disk"
