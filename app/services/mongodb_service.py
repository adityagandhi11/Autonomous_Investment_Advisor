# """MongoDB service for portfolio persistence."""

# import os
# from pymongo import MongoClient
# from datetime import datetime


# mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")

# try:
#     client = MongoClient(mongodb_uri)
#     db = client["myInvestmentAdvisor"]
#     collection = db["portfolio_history"]
# except Exception as e:
#     print(f"Warning: MongoDB connection failed: {e}")
#     db = None
#     collection = None


# def save_portfolio(data: dict) -> bool:
#     """
#     Save portfolio recommendation to MongoDB.
#     """
#     if collection is None:
#         return False

#     try:
#         data["created_at"] = datetime.utcnow()
#         result = collection.insert_one(data)
#         return result.inserted_id is not None
#     except Exception as e:
#         print(f"Error saving portfolio: {e}")
#         return False


# def get_portfolio_history(limit: int = 10) -> list:
#     """
#     Retrieve recent portfolio recommendations from MongoDB.
#     """
#     if collection is None:
#         return []

#     try:
#         return list(collection.find().sort("created_at", -1).limit(limit))
#     except Exception as e:
#         print(f"Error retrieving portfolio history: {e}")
#         return []


"""MongoDB service."""

import os
from datetime import datetime, timezone

from pymongo import MongoClient, ASCENDING


mongodb_uri = os.getenv(
    "MONGODB_URI",
    "mongodb://localhost:27017"
)


try:
    client = MongoClient(mongodb_uri)

    db = client["myInvestmentAdvisor"]

    # Existing collection
    collection = db["portfolio_history"]

    # New collections
    users_collection = db["users"]
    investor_profiles_collection = db["investor_profiles"]

    # Create useful indexes
    users_collection.create_index(
        [("email", ASCENDING)],
        unique=True
    )

    investor_profiles_collection.create_index(
        [("user_id", ASCENDING)],
        unique=True
    )

except Exception as e:
    print(f"Warning: MongoDB connection failed: {e}")

    db = None
    collection = None
    users_collection = None
    investor_profiles_collection = None


# ============================================================
# EXISTING PORTFOLIO FUNCTIONS
# ============================================================

def save_portfolio(data: dict) -> bool:
    """
    Save portfolio recommendation to MongoDB.

    Existing functionality preserved.
    """

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
    """
    Retrieve recent portfolio recommendations.
    """

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


# ============================================================
# USER FUNCTIONS
# ============================================================

def get_user_by_id(user_id: str):
    """Retrieve a user by MongoDB ObjectId."""

    from bson import ObjectId

    if users_collection is None:
        return None

    try:
        return users_collection.find_one(
            {"_id": ObjectId(user_id)}
        )

    except Exception:
        return None


# ============================================================
# INVESTOR PROFILE FUNCTIONS
# ============================================================

def save_investor_profile(
    user_id: str,
    profile: dict
) -> bool:

    if investor_profiles_collection is None:
        return False

    try:
        now = datetime.now(timezone.utc)

        profile["user_id"] = user_id
        profile["updated_at"] = now

        existing = investor_profiles_collection.find_one(
            {"user_id": user_id}
        )

        if existing:
            investor_profiles_collection.update_one(
                {"user_id": user_id},
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
    """Retrieve investor profile."""

    if investor_profiles_collection is None:
        return None

    try:
        return investor_profiles_collection.find_one(
            {"user_id": user_id}
        )

    except Exception as e:
        print(f"Error retrieving investor profile: {e}")
        return None