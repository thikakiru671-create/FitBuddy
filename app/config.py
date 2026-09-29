import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./fitbuddy.db"
    gemini_api_key: str = ""
    workout_model: str = "gemini-2.5-flash"
    ai_mode: str = "gemini"
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


def get_settings() -> Settings:
    return Settings()