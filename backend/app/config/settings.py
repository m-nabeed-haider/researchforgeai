from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMSettings(BaseModel):
    provider: str
    model: str
    openai_api_key: str
    gemini_api_key: str


class Settings(BaseSettings):
    app_name: str = "ResearchForge AI"
    app_version: str = "0.1.0"

    debug: bool = True

    host: str = "0.0.0.0"
    port: int = 8000

    llm: LLMSettings

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()