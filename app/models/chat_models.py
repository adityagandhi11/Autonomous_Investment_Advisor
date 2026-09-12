"""Chat request and response models."""

from typing import List, Literal

from pydantic import BaseModel, Field


class ChatMessageRequest(BaseModel):
    conversation_id: str | None = None
    message: str = Field(..., min_length=1, max_length=4000)

    # Current portfolio context from the dashboard
    investment_goal: str | None = None
    investment_amount: float | None = None
    duration_years: int | None = None
    risk_profile: str | None = None
    portfolio: dict[str, float] | None = None


class ChatMessageResponse(BaseModel):
    conversation_id: str
    role: Literal["assistant"] = "assistant"
    message: str