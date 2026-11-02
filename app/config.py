"""
Application configuration using Pydantic Settings.
"""
import os
from pathlib import Path

try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseModel as BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    APP_NAME: str = "Multiple Disease Prediction System"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = (
        "A production-ready AI-powered web application for predicting "
        "Diabetes, Heart Disease, and Parkinson's Disease using trained "
        "machine learning models."
    )
    DEBUG: bool = os.environ.get("DEBUG", "False").lower() in ("true", "1")
    HOST: str = os.environ.get("HOST", "0.0.0.0")
    PORT: int = int(os.environ.get("PORT", "8000"))

    # Model directory — resolve relative to project root
    MODEL_DIR: str = str(Path(__file__).resolve().parent / "models")

    # CORS
    CORS_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
