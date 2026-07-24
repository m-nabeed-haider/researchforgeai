from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration.
    """

    # ==========================
    # Application
    # ==========================

    app_name: str = "ResearchForge AI"
    app_version: str = "0.1.0"

    debug: bool = True

    host: str = "0.0.0.0"
    port: int = 8000

    # ==========================
    # LLM
    # ==========================

    llm_provider: str = "groq"

    llm_model: str = "llama-3.1-8b-instant"

    groq_api_key: str = ""

    gemini_api_key: str = ""

    openai_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()