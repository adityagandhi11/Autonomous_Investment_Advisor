"""Entry point for the Autonomous Investment Advisor application."""

import uvicorn
import os
from dotenv import load_dotenv


def main():
    """Run the FastAPI application."""
    # Load environment variables
    load_dotenv()
    
    # Verify critical configuration
    if not os.getenv("GROQ_API_KEY"):
        print("⚠️  Warning: GROQ_API_KEY not set in .env")
        print("   The application will fail without it.")
        print("   Get your key from: https://console.groq.com")
    
    # Run the server
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()
