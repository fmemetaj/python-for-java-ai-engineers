from course_kit.loader import load_concept_module

cls = load_concept_module("0_16", "classes")


def test_ticket_label() -> None:
    ticket = cls.make_ticket(7, "Login")
    assert ticket.ticket_id == 7
    assert ticket.subject == "Login"
    assert ticket.label() == "#7 Login"


def test_instances_are_independent() -> None:
    a = cls.Ticket(1, "A")
    b = cls.Ticket(2, "B")
    a.subject = "changed"
    assert b.subject == "B"


def test_private_name_convention() -> None:
    assert cls.is_private_name("_cache") is True
    assert cls.is_private_name("__init__") is False
    assert cls.is_private_name("subject") is False
