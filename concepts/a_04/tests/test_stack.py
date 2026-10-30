from course_kit.loader import load_concept_module

stack = load_concept_module("a_04", "stack")


def test_own_when_evalable() -> None:
    decision = stack.pick_stack(
        own_recall=0.8,
        hosted_available=True,
        can_export=True,
        can_eval=True,
        overlap=0.2,
    )
    assert decision.choice == "own"


def test_hosted_prototype() -> None:
    decision = stack.pick_stack(
        own_recall=0.0,
        hosted_available=True,
        can_export=False,
        can_eval=False,
        overlap=0.0,
    )
    assert decision.choice == "hosted"


def test_hybrid_when_recall_weak() -> None:
    decision = stack.pick_stack(
        own_recall=0.4,
        hosted_available=True,
        can_export=True,
        can_eval=True,
        overlap=0.2,
    )
    assert decision.choice == "hybrid"
