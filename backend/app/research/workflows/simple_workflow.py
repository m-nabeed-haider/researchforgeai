from __future__ import annotations

from backend.app.ai.llms.models import (
    LLMRequest,
    Message,
    MessageRole,
    LLMResponse,
)
from backend.app.ai.llms.service import LLMService
from backend.app.research.models.research_request import ResearchRequest
from backend.app.research.workflows.base import ResearchWorkflow


class SimpleResearchWorkflow(ResearchWorkflow):
    """
    Simple workflow:

    User
        ↓
    LLM
        ↓
    Response
    """

    def __init__(
        self,
        llm_service: LLMService,
    ) -> None:
        self._llm_service = llm_service

    async def run(
        self,
        request: ResearchRequest,
    ) -> LLMResponse:

        llm_request = LLMRequest(
            messages=[
                Message(
                    role=MessageRole.USER,
                    content=request.query,
                )
            ]
        )

        return await self._llm_service.invoke(llm_request)