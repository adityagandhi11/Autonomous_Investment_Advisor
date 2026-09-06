from pydantic import BaseModel
from typing import List, Optional


class InvestmentRequest(BaseModel):
    """API request model for investment advisor."""
    user_goal: str
    investment_amount: float
    duration_years: int


class RiskProfileRequest(BaseModel):
    age: int
    income: float
    goals: List[str]


class PortfolioRequest(BaseModel):
    risk_score: int
    capital: float
    symbols: Optional[List[str]] = None
