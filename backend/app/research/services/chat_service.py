from __future__ import annotations

from backend.app.ai.llms.models import (
    LLMRequest,
    LLMResponse,
    Message,
    MessageRole,
)
from backend.app.ai.llms.service import LLMService


class ChatService:
    """
    Application service for chat interactions.
    """

    def __init__(
        self,
        llm_service: LLMService,
    ) -> None:
        self._llm_service = llm_service

    async def chat(
        self,
        message: str,
    ) -> LLMResponse:

        request = LLMRequest(
            messages=[
                Message(
                    role=MessageRole.USER,
                    content=message,
                )
            ]
        )

        return await self._llm_service.invoke(request)