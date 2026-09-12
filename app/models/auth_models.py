"""Authentication request and response models."""

from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    """Request body for user registration."""

    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class LoginRequest(BaseModel):
    """Request body for user login."""

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Public user information."""

    user_id: str
    name: str
    email: str
    created_at: str


class AuthResponse(BaseModel):
    """Authentication response."""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    """Decoded JWT data."""

    user_id: Optional[str] = None
    email: Optional[str] = None