"""Authentication API routes."""

from datetime import datetime

from fastapi import APIRouter, HTTPException

from app.models.auth_models import (
    AuthResponse,
    LoginRequest,
    SignupRequest,
    UserResponse
)

from app.services.auth_service import (
    authenticate_user,
    create_access_token,
    create_user
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/signup",
    response_model=AuthResponse
)
async def signup(request: SignupRequest):

    try:
        user = create_user(
            name=request.name,
            email=request.email,
            password=request.password
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    token = create_access_token(
        user_id=user["user_id"],
        email=user["email"]
    )

    created_at = user["created_at"]

    if isinstance(created_at, datetime):
        created_at = created_at.isoformat()

    return AuthResponse(
        access_token=token,
        user=UserResponse(
            user_id=user["user_id"],
            name=user["name"],
            email=user["email"],
            created_at=created_at
        )
    )


@router.post(
    "/login",
    response_model=AuthResponse
)
async def login(request: LoginRequest):

    user = authenticate_user(
        email=request.email,
        password=request.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        user_id=user["user_id"],
        email=user["email"]
    )

    created_at = user["created_at"]

    if isinstance(created_at, datetime):
        created_at = created_at.isoformat()

    return AuthResponse(
        access_token=token,
        user=UserResponse(
            user_id=user["user_id"],
            name=user["name"],
            email=user["email"],
            created_at=created_at
        )
    )