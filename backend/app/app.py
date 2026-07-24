from fastapi import FastAPI

from backend.app.api.router import api_router
from backend.app.config.settings import get_settings
from backend.app.logging_config.logger import configure_logger


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    configure_logger()

    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
    )

    app.include_router(api_router)

    return app