from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.app.api.router import api_router
from backend.app.core.container import Container


@asynccontextmanager
async def lifespan(
    app: FastAPI,
):

    container = Container()

    app.state.container = container

    yield

    await container.close()


def create_app() -> FastAPI:

    app = FastAPI(
        title="ResearchForge AI",
        lifespan=lifespan,
    )

    app.include_router(
        api_router,
    )

    return app