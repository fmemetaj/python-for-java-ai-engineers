"""Validated models for the simulated helpdesk."""

from pydantic import BaseModel, Field


class Ticket(BaseModel):
    id: int = Field(gt=0)
    subject: str = Field(min_length=2)
    body: str = Field(min_length=3)


class ReplyProposal(BaseModel):
    ticket_id: int
    category: str
    suggested_reply: str
    approved: bool = False
