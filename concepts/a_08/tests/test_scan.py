from course_kit.loader import load_concept_module

scan = load_concept_module("a_08", "scan")


def test_clean_responses() -> None:
    source = "client.responses.create(model='gpt-4.1-mini', input='hi')"
    assert scan.is_clean(source) is True
    assert scan.findings(source) == []


def test_flags_0x_helper() -> None:
    source = "openai.ChatCompletion.create(model='gpt-3.5-turbo')"
    hits = scan.findings(source)
    assert hits
    assert hits[0].line == 1
    assert "ChatCompletion.create" in hits[0].pattern


def test_does_not_flag_current_chat() -> None:
    source = "client.chat.completions.create(model='gpt-4.1-mini', messages=[])"
    assert scan.is_clean(source) is True
