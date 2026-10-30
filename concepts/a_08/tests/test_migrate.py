from course_kit.loader import load_concept_module

migrate = load_concept_module("a_08", "migrate")


def test_classify() -> None:
    assert migrate.classify("client.responses.create()") == "ok"
    assert migrate.classify("client.beta.threads.create()") == "sunset"
    assert migrate.classify("openai.ChatCompletion.create()") == "legacy-0x"
    assert migrate.classify("# Assistants API was sunset") == "sunset"
