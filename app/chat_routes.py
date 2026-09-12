"""Chat API routes."""

from fastapi import APIRouter, Depends, HTTPException

from app.models.chat_models import (
    ChatMessageRequest,
    ChatMessageResponse,
)
from app.services.chat_service import generate_chat_response
from app.utils.auth_dependencies import get_current_user


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post(
    "",
    response_model=ChatMessageResponse
)
async def chat(
    request: ChatMessageRequest,
    current_user=Depends(get_current_user)
):
    """Send a message to the investment advisor."""

    try:
        user_id = str(current_user["_id"])

        assistant_message, conversation_id = generate_chat_response(
            user_id=user_id,
            message=request.message,
            conversation_id=request.conversation_id,
            investment_goal=request.investment_goal,
            investment_amount=request.investment_amount,
            duration_years=request.duration_years,
            risk_profile=request.risk_profile,
            portfolio=request.portfolio,
        )

        return ChatMessageResponse(
            conversation_id=conversation_id,
            message=assistant_message
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chat error: {str(e)}"
        )