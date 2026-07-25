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

    response, results = await container.chat_service.chat(
        request.messages,
    )

    return ChatResponse(
        response=response.content,
        sources=[
            ChatSource(
                name=result.source,
                url=result.url,
            )
            for result in results
        ],
    )