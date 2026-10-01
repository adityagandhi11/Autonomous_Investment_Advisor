# from fastapi import APIRouter, Depends, HTTPException

# from app.models.chat_models import (
#     ChatMessageRequest,
#     ChatMessageResponse
# )

# from app.services.chat_service import (
#     generate_chat_response
# )

# from app.utils.auth_dependencies import (
#     get_current_user
# )


# router = APIRouter(
#     prefix="/chat",
#     tags=["Chat"]
# )


# @router.post(
#     "",
#     response_model=ChatMessageResponse
# )
# async def chat(
#     request: ChatMessageRequest,
#     current_user=Depends(get_current_user)
# ):
#     try:
#         user_id = str(
#             current_user["_id"]
#         )

#         (
#             assistant_message,
#             conversation_id,
#             chat_intent,
#             portfolio_updated,
#             updated_analysis
#         ) = generate_chat_response(
#             user_id=user_id,
#             message=request.message,
#             conversation_id=request.conversation_id,
#             investment_goal=request.investment_goal,
#             investment_amount=request.investment_amount,
#             duration_years=request.duration_years,
#             risk_profile=request.risk_profile,
#             portfolio=request.portfolio,
#         )

#         return ChatMessageResponse(
#             conversation_id=conversation_id,
#             message=assistant_message,
#             intent=chat_intent["intent"],
#             changes=chat_intent["changes"],
#             portfolio_updated=portfolio_updated,
#             updated_analysis=updated_analysis
#         )

#     except ValueError as e:
#         raise HTTPException(
#             status_code=404,
#             detail=str(e)
#         )

#     except Exception as e:
#         import traceback

#         traceback.print_exc()

#         raise HTTPException(
#             status_code=500,
#             detail=f"Chat error: {str(e)}"
#         )

from fastapi import APIRouter, Depends, HTTPException

from app.models.chat_models import (
    ChatMessageRequest,
    ChatMessageResponse
)

from app.services.chat_service import (
    generate_chat_response
)

from app.services.mongodb_service import (
    get_user_chat_conversations,
    get_chat_conversation
)

from app.utils.auth_dependencies import (
    get_current_user
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


# ---------------------------------------------------------------------------
# Send chat message
# ---------------------------------------------------------------------------

@router.post(
    "",
    response_model=ChatMessageResponse
)
async def chat(
    request: ChatMessageRequest,
    current_user=Depends(get_current_user)
):
    try:
        user_id = str(
            current_user["_id"]
        )

        (
            assistant_message,
            conversation_id,
            chat_intent,
            portfolio_updated,
            updated_analysis
        ) = generate_chat_response(
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
            message=assistant_message,
            intent=chat_intent["intent"],
            changes=chat_intent["changes"],
            portfolio_updated=portfolio_updated,
            updated_analysis=updated_analysis
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except Exception as e:
        import traceback

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"Chat error: {str(e)}"
        )


# ---------------------------------------------------------------------------
# Get user's chat history
# ---------------------------------------------------------------------------

@router.get(
    "/conversations"
)
async def get_chat_history(
    current_user=Depends(get_current_user)
):
    """
    Retrieve the authenticated user's chat conversations.

    Conversations are sorted by most recently updated first.
    Message contents are not returned by this endpoint.
    """

    try:
        user_id = str(
            current_user["_id"]
        )

        conversations = get_user_chat_conversations(
            user_id=user_id,
            limit=50
        )

        result = []

        for conversation in conversations:
            result.append({
                "conversation_id": str(
                    conversation["_id"]
                ),
                "title": conversation.get(
                    "title",
                    "New investment conversation"
                ),
                "created_at": (
                    conversation["created_at"].isoformat()
                    if conversation.get("created_at")
                    else None
                ),
                "updated_at": (
                    conversation["updated_at"].isoformat()
                    if conversation.get("updated_at")
                    else None
                )
            })

        return {
            "conversations": result
        }

    except Exception as e:
        import traceback

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve chat history: {str(e)}"
        )


# ---------------------------------------------------------------------------
# Get one conversation
# ---------------------------------------------------------------------------

@router.get(
    "/conversations/{conversation_id}"
)
async def get_conversation(
    conversation_id: str,
    current_user=Depends(get_current_user)
):
    """
    Retrieve a complete conversation belonging to the
    authenticated user.
    """

    try:
        user_id = str(
            current_user["_id"]
        )

        conversation = get_chat_conversation(
            conversation_id=conversation_id,
            user_id=user_id
        )

        if not conversation:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found."
            )

        return {
            "conversation_id": str(
                conversation["_id"]
            ),
            "title": conversation.get(
                "title",
                "New investment conversation"
            ),
            "created_at": (
                conversation["created_at"].isoformat()
                if conversation.get("created_at")
                else None
            ),
            "updated_at": (
                conversation["updated_at"].isoformat()
                if conversation.get("updated_at")
                else None
            ),
            "messages": [
                {
                    "role": message.get(
                        "role",
                        "user"
                    ),
                    "content": message.get(
                        "content",
                        ""
                    ),
                    "timestamp": (
                        message["timestamp"].isoformat()
                        if message.get("timestamp")
                        else None
                    )
                }
                for message in conversation.get(
                    "messages",
                    []
                )
            ]
        }

    except HTTPException:
        raise

    except Exception as e:
        import traceback

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve conversation: {str(e)}"
        )