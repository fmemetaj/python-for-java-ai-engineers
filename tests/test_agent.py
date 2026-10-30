"""Regression tests for the simulated assistant."""

import asyncio
import pytest
from pydantic import ValidationError
from mini_agent import Ticket, ReplyProposal, classify_ticket, prepare_reply, simulate_send


def test_access_classification():
    assert classify_ticket(Ticket(id=1, subject="Login", body="Can't log in")) == "access"


def test_billing_classification():
    assert (
        classify_ticket(Ticket(id=2, subject="Invoice", body="Invoice not available")) == "billing"
    )


def test_general_classification():
    assert classify_ticket(Ticket(id=3, subject="Feature", body="Dark mode request")) == "general"


def test_validation_rejects_invalid_id():
    with pytest.raises(ValidationError):
        Ticket(id=0, subject="Help", body="Please assist")


def test_validation_rejects_short_body():
    with pytest.raises(ValidationError):
        Ticket(id=1, subject="Help", body="x")


def test_proposal_unapproved_by_default():
    proposal = asyncio.run(prepare_reply(Ticket(id=4, subject="Account", body="Cannot sign in")))
    assert proposal.approved is False


def test_cannot_send_without_approval():
    proposal = ReplyProposal(ticket_id=1, category="general", suggested_reply="Hello")
    assert simulate_send(proposal, approved=False)["would_send"] is False


def test_approved_send_is_still_only_simulated():
    proposal = ReplyProposal(ticket_id=1, category="general", suggested_reply="Hello")
    assert simulate_send(proposal, approved=True)["would_send"] is True


def test_registry_decorator_registers_classify() -> None:
    from mini_agent.tools import registry

    assert "classify" in registry.names()
    assert registry.call("classify", "cannot log in please help") == "access"
    assert registry.call("kb_hint", "billing") == "Please check your billing portal."


def test_registry_unknown_tool_lists_names() -> None:
    from mini_agent.tools import registry

    with pytest.raises(KeyError, match="unknown tool"):
        registry.get("not-a-tool")
