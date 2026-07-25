from __future__ import annotations

from backend.app.ai.llms.models import LLMRequest
from backend.app.ai.llms.service import LLMService

from backend.app.ai.prompts import PromptBuilder

from backend.app.ai.search import SearchService
from backend.app.ai.search.formatter import (
    format_search_context,
)
from backend.app.ai.search.models import SearchRequest

from backend.app.research.routing import (
    LLMResearchRouter,
    ResearchStrategy,
)
from backend.app.research.state import ResearchState
from backend.app.research.workflows.base import (
    ResearchWorkflow,
)


class SimpleResearchWorkflow(ResearchWorkflow):
    """
    Basic research workflow.
    """

    def __init__(
        self,
        llm_service: LLMService,
        prompt_builder: PromptBuilder,
        search_service: SearchService,
        router: LLMResearchRouter,
    ) -> None:

        self._llm_service = llm_service
        self._prompt_builder = prompt_builder
        self._search_service = search_service
        self._router = router

    async def run(
        self,
        state: ResearchState,
    ) -> ResearchState:

        strategy = await self._router.route(
            state,
        )

        if strategy == ResearchStrategy.WEB_SEARCH:

            query = state.messages[-1].content

            state.search_results = await self._search_service.search(
                SearchRequest(
                    query=query,
                    max_results=3,
                )
            )

            state.context = format_search_context(
                state.search_results,
            )

        messages = self._prompt_builder.build(
            conversation=state.messages,
            context=state.context,
        )

        state.response = await self._llm_service.invoke(
            LLMRequest(
                messages=messages,
                max_tokens=180,
            )
        )

        return state