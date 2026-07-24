from fastapi import APIRouter, Depends

from backend.app.api.schemas.chat import ChatRequest, ChatResponse
from backend.app.core.container import Container
from backend.app.core.container.dependencies import get_container

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.post("")
async def chat(
    request: ChatRequest,
    container: Container = Depends(get_container),
) -> ChatResponse:

    result = await container.chat_service.chat(
        request.messages,
    )

    return ChatResponse(
        response=result.content,
    )