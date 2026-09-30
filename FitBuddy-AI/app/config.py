from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FitBuddy – AI Fitness Plan Generator"

    gemini_api_key: str | None = None

    gemini_workout_model: str = "gemini-3.8-flash"
    gemini_tip_model: str = "gemini-3.5-flash-lite"

    database_url: str = "sqlite:///./fitbuddy.db"

    mock_ai: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()