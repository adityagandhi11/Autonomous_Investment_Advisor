"""Investor profile request and response models."""

from typing import List, Optional

from pydantic import BaseModel, Field


class InvestorProfileRequest(BaseModel):
    """Investor financial and investment profile."""

    age: int = Field(..., ge=18, le=100)

    annual_income: float = Field(..., ge=0)
    monthly_expenses: float = Field(..., ge=0)
    emergency_fund: float = Field(..., ge=0)

    investment_amount: float = Field(..., ge=0)
    monthly_sip: float = Field(default=0, ge=0)

    investment_horizon_years: int = Field(..., ge=1, le=100)

    investment_goal: str = Field(
        ...,
        min_length=2,
        max_length=200
    )

    investment_experience: str = Field(
        ...,
        min_length=2,
        max_length=50
    )

    risk_tolerance: Optional[str] = None
    risk_capacity: Optional[str] = None
    risk_profile: Optional[str] = None

    preferred_asset_classes: List[str] = Field(default_factory=list)
    excluded_assets: List[str] = Field(default_factory=list)


class InvestorProfileResponse(InvestorProfileRequest):
    """Investor profile returned from the API."""

    user_id: str
    created_at: str
    updated_at: str