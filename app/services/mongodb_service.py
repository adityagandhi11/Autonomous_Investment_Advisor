"""MongoDB service for portfolio persistence."""

import os
from pymongo import MongoClient
from datetime import datetime


mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")

try:
    client = MongoClient(mongodb_uri)
    db = client["myInvestmentAdvisor"]
    collection = db["portfolio_history"]
except Exception as e:
    print(f"Warning: MongoDB connection failed: {e}")
    db = None
    collection = None


def save_portfolio(data: dict) -> bool:
    """
    Save portfolio recommendation to MongoDB.
    """
    if collection is None:
        return False

    try:
        data["created_at"] = datetime.utcnow()
        result = collection.insert_one(data)
        return result.inserted_id is not None
    except Exception as e:
        print(f"Error saving portfolio: {e}")
        return False


def get_portfolio_history(limit: int = 10) -> list:
    """
    Retrieve recent portfolio recommendations from MongoDB.
    """
    if collection is None:
        return []

    try:
        return list(collection.find().sort("created_at", -1).limit(limit))
    except Exception as e:
        print(f"Error retrieving portfolio history: {e}")
        return []
