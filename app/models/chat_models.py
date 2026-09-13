"""Chat request, response, and intent models."""

from typing import Literal
from pydantic import BaseModel, Field


class PortfolioChanges(BaseModel):
    investment_amount: float | None = None
    duration_years: int | None = None
    risk_profile: Literal["low", "moderate", "high"] | None = None
    investment_goal: str | None = None


class ChatIntent(BaseModel):
    intent: Literal["informational", "modify_portfolio"]
    changes: PortfolioChanges = Field(
        default_factory=PortfolioChanges
    )


class ChatMessageRequest(BaseModel):
    conversation_id: str | None = None
    message: str = Field(
        ...,
        min_length=1,
        max_length=4000
    )

    investment_goal: str | None = None
    investment_amount: float | None = None
    duration_years: int | None = None
    risk_profile: str | None = None
    portfolio: dict[str, float] | None = None


class ChatMessageResponse(BaseModel):
    conversation_id: str

    role: Literal["assistant"] = "assistant"

    message: str

    intent: Literal[
        "informational",
        "modify_portfolio"
    ] = "informational"

    changes: PortfolioChanges = Field(
        default_factory=PortfolioChanges
    )

    portfolio_updated: bool = False

    # Complete updated investment analysis.
    updated_analysis: dict | None = None