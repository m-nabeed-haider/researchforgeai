from __future__ import annotations

from backend.app.research.state import ResearchState
from backend.app.research.workflows.base import ResearchWorkflow

from backend.app.ai.llms.models import (
    LLMResponse,
    Message,
)

from backend.app.ai.search.models import SearchResult


class ChatService:
    """
    Coordinates chat requests.
    """

    def __init__(
        self,
        workflow: ResearchWorkflow,
    ) -> None:

        self._workflow = workflow

    async def chat(
        self,
        messages: list[Message],
    ) -> tuple[
        LLMResponse,
        list[SearchResult],
    ]:

        state = ResearchState(
            messages=messages,
        )

        state = await self._workflow.run(
            state,
        )

        results = []

        if state.search_results is not None:
            results = state.search_results.results

        return (
            state.response,
            results,
        )