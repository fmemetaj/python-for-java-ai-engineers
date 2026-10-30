import pytest
from course_kit.loader import load_concept_module

layers = load_concept_module("7_02", "layers")


def test_order() -> None:
    names = layers.architecture_layers()
    assert names == ["http", "security", "budget", "rag", "agent", "observe", "evals"]


def test_index() -> None:
    assert layers.layer_index("http") == 0
    assert layers.layer_index("evals") == 6
    assert layers.layer_index("rag") < layers.layer_index("agent")
    with pytest.raises(KeyError):
        layers.layer_index("assistants-api")
