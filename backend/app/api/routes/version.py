from fastapi import APIRouter

from backend.app.core.config.settings import get_settings

router = APIRouter(tags=["System"])


@router.get("/version")
async def version() -> dict[str, str]:
    settings = get_settings()
    return {"version": settings.app_version}
