from course_kit.loader import load_concept_module

memory = load_concept_module("5_03", "memory")


def test_token_count() -> None:
    assert memory.token_count("") == 0
    assert memory.token_count("abcd") == 1
    assert memory.token_count("abcdefgh") == 2


def test_add_and_used_tokens() -> None:
    store = memory.WorkingMemory(budget_tokens=100)
    item = store.add("observation", "abcd")
    assert item.tokens == 1
    assert store.used_tokens == 1


def test_trim_drops_oldest_unpinned() -> None:
    store = memory.WorkingMemory(budget_tokens=2)
    store.add("user", "PINN", pinned=True)  # 1 token
    store.add("observation", "aaaa")  # 1 token
    store.add("observation", "bbbb")  # 1 token — over budget
    texts = [item.text for item in store.items]
    assert "PINN" in texts
    assert "aaaa" not in texts
    assert "bbbb" in texts
    assert store.used_tokens <= 2


def test_pinned_only_can_exceed_budget() -> None:
    store = memory.WorkingMemory(budget_tokens=1)
    store.add("user", "abcdefgh", pinned=True)  # 2 tokens
    assert len(store.items) == 1
    assert store.items[0].pinned is True
