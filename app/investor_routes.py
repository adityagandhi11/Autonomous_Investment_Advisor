"""Investor profile API routes."""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from app.models.investor_models import (
    InvestorProfileRequest,
    InvestorProfileResponse
)

from app.services.mongodb_service import (
    get_investor_profile,
    save_investor_profile
)

from app.utils.auth_dependencies import get_current_user


router = APIRouter(
    prefix="/investor-profile",
    tags=["Investor Profile"]
)


@router.get(
    "",
    response_model=InvestorProfileResponse | None
)
async def get_profile(
    current_user: dict = Depends(get_current_user)
):
    """Get the authenticated user's investor profile."""

    user_id = str(current_user["_id"])

    profile = get_investor_profile(user_id)

    if not profile:
        return None

    # MongoDB ObjectId is not part of our API response
    profile.pop("_id", None)

    # Convert datetime objects to ISO strings
    for field in ["created_at", "updated_at"]:
        if isinstance(profile.get(field), datetime):
            profile[field] = profile[field].isoformat()

    return profile


@router.post(
    "",
    response_model=InvestorProfileResponse
)
async def create_or_update_profile(
    request: InvestorProfileRequest,
    current_user: dict = Depends(get_current_user)
):
    """Create or update the authenticated user's investor profile."""

    user_id = str(current_user["_id"])

    profile_data = request.model_dump()

    success = save_investor_profile(
        user_id=user_id,
        profile=profile_data
    )

    if not success:
        raise HTTPException(
            status_code=500,
            detail="Unable to save investor profile"
        )

    profile = get_investor_profile(user_id)

    if not profile:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve saved profile"
        )

    # MongoDB ObjectId is not part of our API response
    profile.pop("_id", None)

    # Convert datetime objects to ISO strings
    for field in ["created_at", "updated_at"]:
        if isinstance(profile.get(field), datetime):
            profile[field] = profile[field].isoformat()

    return profile