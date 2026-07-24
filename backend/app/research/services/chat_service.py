from __future__ import annotations

from backend.app.ai.llms.models import LLMResponse
from backend.app.research.models.research_request import ResearchRequest
from backend.app.research.workflows.base import ResearchWorkflow


class ChatService:
    """
    Application service responsible for handling chat requests.
    """

    def __init__(
        self,
        workflow: ResearchWorkflow,
    ) -> None:
        self._workflow = workflow

    async def chat(
        self,
        message: str,
    ) -> LLMResponse:

        request = ResearchRequest(
            query=message,
        )

        return await self._workflow.run(request)