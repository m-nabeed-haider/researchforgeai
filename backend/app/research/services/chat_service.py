from __future__ import annotations

from backend.app.ai.llms.models import (
    LLMResponse,
    Message,
)

from backend.app.research.models.research_request import ResearchRequest
from backend.app.research.workflows.base import ResearchWorkflow


class ChatService:
    """
    Application service responsible for chat requests.
    """

    def __init__(
        self,
        workflow: ResearchWorkflow,
    ) -> None:
        self._workflow = workflow

    async def chat(
        self,
        messages: list[Message],
    ) -> LLMResponse:

        request = ResearchRequest(
            messages=messages,
        )

        return await self._workflow.run(request)