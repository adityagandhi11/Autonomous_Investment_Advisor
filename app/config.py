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
    jwt_secret_key: str = ""
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
