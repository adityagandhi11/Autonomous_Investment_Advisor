# """MongoDB service."""

# import os
# from datetime import datetime, timezone

# from pymongo import MongoClient, ASCENDING


# mongodb_uri = os.getenv(
#     "MONGODB_URI",
#     "mongodb://localhost:27017"
# )


# try:
#     client = MongoClient(mongodb_uri)

#     db = client["myInvestmentAdvisor"]

#     # Existing collection
#     collection = db["portfolio_history"]

#     # New collections
#     users_collection = db["users"]
#     investor_profiles_collection = db["investor_profiles"]

#     # Create useful indexes
#     users_collection.create_index(
#         [("email", ASCENDING)],
#         unique=True
#     )

#     investor_profiles_collection.create_index(
#         [("user_id", ASCENDING)],
#         unique=True
#     )

# except Exception as e:
#     print(f"Warning: MongoDB connection failed: {e}")

#     db = None
#     collection = None
#     users_collection = None
#     investor_profiles_collection = None


# # ============================================================
# # EXISTING PORTFOLIO FUNCTIONS
# # ============================================================

# def save_portfolio(data: dict) -> bool:
#     """
#     Save portfolio recommendation to MongoDB.

#     Existing functionality preserved.
#     """

#     if collection is None:
#         return False

#     try:
#         data["created_at"] = datetime.now(timezone.utc)

#         result = collection.insert_one(data)

#         return result.inserted_id is not None

#     except Exception as e:
#         print(f"Error saving portfolio: {e}")
#         return False


# def get_portfolio_history(limit: int = 10) -> list:
#     """
#     Retrieve recent portfolio recommendations.
#     """

#     if collection is None:
#         return []

#     try:
#         return list(
#             collection
#             .find()
#             .sort("created_at", -1)
#             .limit(limit)
#         )

#     except Exception as e:
#         print(f"Error retrieving portfolio: {e}")
#         return []


# # ============================================================
# # USER FUNCTIONS
# # ============================================================

# def get_user_by_id(user_id: str):
#     """Retrieve a user by MongoDB ObjectId."""

#     from bson import ObjectId

#     if users_collection is None:
#         return None

#     try:
#         return users_collection.find_one(
#             {"_id": ObjectId(user_id)}
#         )

#     except Exception:
#         return None


# # ============================================================
# # INVESTOR PROFILE FUNCTIONS
# # ============================================================

# def save_investor_profile(
#     user_id: str,
#     profile: dict
# ) -> bool:

#     if investor_profiles_collection is None:
#         return False

#     try:
#         now = datetime.now(timezone.utc)

#         profile["user_id"] = user_id
#         profile["updated_at"] = now

#         existing = investor_profiles_collection.find_one(
#             {"user_id": user_id}
#         )

#         if existing:
#             investor_profiles_collection.update_one(
#                 {"user_id": user_id},
#                 {
#                     "$set": profile,
#                     "$setOnInsert": {
#                         "created_at": now
#                     }
#                 }
#             )
#         else:
#             profile["created_at"] = now

#             investor_profiles_collection.insert_one(
#                 profile
#             )

#         return True

#     except Exception as e:
#         print(f"Error saving investor profile: {e}")
#         return False


# def get_investor_profile(user_id: str):
#     """Retrieve investor profile."""

#     if investor_profiles_collection is None:
#         return None

#     try:
#         return investor_profiles_collection.find_one(
#             {"user_id": user_id}
#         )

#     except Exception as e:
#         print(f"Error retrieving investor profile: {e}")
#         return None


"""MongoDB service."""

import os
from datetime import datetime, timezone

from pymongo import MongoClient, ASCENDING


# ---------------------------------------------------------------------------
# MongoDB connection
# ---------------------------------------------------------------------------

mongodb_uri = os.getenv(
    "MONGODB_URI",
    "mongodb://localhost:27017"
)

try:
    client = MongoClient(mongodb_uri)

    db = client["myInvestmentAdvisor"]

    # Existing collections
    collection = db["portfolio_history"]
    users_collection = db["users"]
    investor_profiles_collection = db["investor_profiles"]

    # Chat collection
    chat_conversations_collection = db["chat_conversations"]

    # Indexes
    users_collection.create_index(
        [("email", ASCENDING)],
        unique=True
    )

    investor_profiles_collection.create_index(
        [("user_id", ASCENDING)],
        unique=True
    )

    chat_conversations_collection.create_index(
        [("user_id", ASCENDING)]
    )

    chat_conversations_collection.create_index(
        [("updated_at", -1)]
    )

except Exception as e:
    print(f"Warning: MongoDB connection failed: {e}")

    db = None
    collection = None
    users_collection = None
    investor_profiles_collection = None
    chat_conversations_collection = None


# ---------------------------------------------------------------------------
# Portfolio history
# ---------------------------------------------------------------------------

def save_portfolio(data: dict) -> bool:
    """Save a generated portfolio to MongoDB."""

    if collection is None:
        return False

    try:
        data["created_at"] = datetime.now(timezone.utc)

        result = collection.insert_one(data)

        return result.inserted_id is not None

    except Exception as e:
        print(f"Error saving portfolio: {e}")
        return False


def get_portfolio_history(limit: int = 10) -> list:
    """Retrieve recent portfolio history."""

    if collection is None:
        return []

    try:
        return list(
            collection
            .find()
            .sort("created_at", -1)
            .limit(limit)
        )

    except Exception as e:
        print(f"Error retrieving portfolio: {e}")
        return []


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------

def get_user_by_id(user_id: str):
    """Retrieve a user by MongoDB ObjectId."""

    from bson import ObjectId

    if users_collection is None:
        return None

    try:
        return users_collection.find_one(
            {
                "_id": ObjectId(user_id)
            }
        )

    except Exception:
        return None


# ---------------------------------------------------------------------------
# Investor profile
# ---------------------------------------------------------------------------

def save_investor_profile(
    user_id: str,
    profile: dict
) -> bool:
    """Create or update an investor profile."""

    if investor_profiles_collection is None:
        return False

    try:
        now = datetime.now(timezone.utc)

        profile["user_id"] = user_id
        profile["updated_at"] = now

        existing = investor_profiles_collection.find_one(
            {
                "user_id": user_id
            }
        )

        if existing:
            investor_profiles_collection.update_one(
                {
                    "user_id": user_id
                },
                {
                    "$set": profile,
                    "$setOnInsert": {
                        "created_at": now
                    }
                }
            )

        else:
            profile["created_at"] = now

            investor_profiles_collection.insert_one(
                profile
            )

        return True

    except Exception as e:
        print(f"Error saving investor profile: {e}")
        return False


def get_investor_profile(user_id: str):
    """Retrieve an investor profile by user ID."""

    if investor_profiles_collection is None:
        return None

    try:
        return investor_profiles_collection.find_one(
            {
                "user_id": user_id
            }
        )

    except Exception as e:
        print(f"Error retrieving investor profile: {e}")
        return None


# ---------------------------------------------------------------------------
# Chat conversations
# ---------------------------------------------------------------------------

def create_chat_conversation(
    user_id: str
) -> str | None:
    """
    Create a new chat conversation.

    Returns:
        MongoDB conversation ID as a string, or None if creation fails.
    """

    if chat_conversations_collection is None:
        return None

    try:
        now = datetime.now(timezone.utc)

        result = chat_conversations_collection.insert_one(
            {
                "user_id": user_id,
                "title": "New investment conversation",
                "messages": [],
                "created_at": now,
                "updated_at": now
            }
        )

        if result.inserted_id is None:
            return None

        return str(result.inserted_id)

    except Exception as e:
        print(f"Error creating chat conversation: {e}")
        return None


def save_chat_message(
    conversation_id: str,
    user_id: str,
    role: str,
    content: str
) -> bool:
    """
    Save a user or assistant message to a conversation.

    The user_id check ensures that one user cannot write to
    another user's conversation.
    """

    if chat_conversations_collection is None:
        return False

    try:
        from bson import ObjectId

        now = datetime.now(timezone.utc)

        result = chat_conversations_collection.update_one(
            {
                "_id": ObjectId(conversation_id),
                "user_id": user_id
            },
            {
                "$push": {
                    "messages": {
                        "role": role,
                        "content": content,
                        "timestamp": now
                    }
                },
                "$set": {
                    "updated_at": now
                }
            }
        )

        return result.modified_count > 0

    except Exception as e:
        print(f"Error saving chat message: {e}")
        return False


def get_chat_conversation(
    conversation_id: str,
    user_id: str
):
    """
    Retrieve one conversation belonging to a specific user.

    Returns:
        Conversation document or None.
    """

    if chat_conversations_collection is None:
        return None

    try:
        from bson import ObjectId

        return chat_conversations_collection.find_one(
            {
                "_id": ObjectId(conversation_id),
                "user_id": user_id
            }
        )

    except Exception as e:
        print(f"Error retrieving chat conversation: {e}")
        return None


def get_user_chat_conversations(
    user_id: str,
    limit: int = 20
) -> list:
    """
    Retrieve a user's recent conversations.

    Messages are intentionally excluded because this function
    is meant for listing conversations in a future chat sidebar.
    """

    if chat_conversations_collection is None:
        return []

    try:
        return list(
            chat_conversations_collection
            .find(
                {
                    "user_id": user_id
                },
                {
                    "messages": 0
                }
            )
            .sort(
                "updated_at",
                -1
            )
            .limit(limit)
        )

    except Exception as e:
        print(f"Error retrieving chat conversations: {e}")
        return []


def update_chat_title(
    conversation_id: str,
    user_id: str,
    title: str
) -> bool:
    """Update the title of a user's conversation."""

    if chat_conversations_collection is None:
        return False

    try:
        from bson import ObjectId

        result = chat_conversations_collection.update_one(
            {
                "_id": ObjectId(conversation_id),
                "user_id": user_id
            },
            {
                "$set": {
                    "title": title,
                    "updated_at": datetime.now(timezone.utc)
                }
            }
        )

        return result.modified_count > 0

    except Exception as e:
        print(f"Error updating chat title: {e}")
        return False
