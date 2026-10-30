from course_kit.loader import load_concept_module

thr = load_concept_module("0_28", "threads")


def test_run_parallel_preserves_order() -> None:
    def stamp(item: int) -> str:
        return f"t{item}"

    assert thr.run_parallel(stamp, [3, 1, 2]) == ["t3", "t1", "t2"]
    assert thr.run_parallel(stamp, []) == []


def test_run_parallel_maps_values() -> None:
    assert thr.run_parallel(lambda n: n * n, [1, 2, 3, 4], max_workers=2) == [1, 4, 9, 16]
