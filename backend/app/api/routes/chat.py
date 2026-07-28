from fastapi import (
    APIRouter,
    Depends,
)

from backend.app.api.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ChatSource,
)

from backend.app.core.container.dependencies import (
    get_container,
)
from backend.app.core.container import Container


router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
    container: Container = Depends(
        get_container,
    ),
) -> ChatResponse:

    result = await container.chat_service.chat(
        session_id=request.session_id,
        messages=[request.message],
    )

    return ChatResponse(
        response=result.response.content,
        sources=[
            ChatSource(
                name=source.source,
                url=source.url,
            )
            for source in result.sources
        ],
    )