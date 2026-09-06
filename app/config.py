"""Configuration management."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables."""
    debug: bool = True
    mongodb_uri: str = "mongodb://localhost:27017"
    groq_api_key: str = ""
    groq_model: str = "openai/gpt-oss-120b"
    alpha_vantage_key: str = ""
    news_api_key: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
