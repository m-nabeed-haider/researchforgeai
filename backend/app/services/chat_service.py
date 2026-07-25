from __future__ import annotations

from backend.app.ai.llms.models import Message
from backend.app.research.engine import ResearchState
from backend.app.research.engine import ResearchWorkflow
from backend.app.research.models import ChatResult

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
    ) -> ChatResult:

        state = ResearchState(
            messages=messages,
        )

        state = await self._workflow.run(
            state,
        )

        sources = []

        if state.search_results:
            sources = state.search_results.results


        return ChatResult(
            response=state.response,
            sources=sources,
        )