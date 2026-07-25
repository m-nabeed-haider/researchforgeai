from __future__ import annotations

from backend.app.ai.llms.models import (
    LLMRequest,
    LLMResponse,
)
from backend.app.ai.llms.service import LLMService

from backend.app.ai.prompts import PromptBuilder

from backend.app.ai.search import SearchService
from backend.app.ai.search.models import SearchRequest
from backend.app.ai.search.formatting import (
    SearchContextFormatter,
)
from backend.app.ai.search.ranking import SearchRankingService

from backend.app.research.routing import (
    ResearchRouter,
    ResearchStrategy,
)

from backend.app.research.engine import ResearchState
from backend.app.research.engine import ResearchWorkflow


class SimpleResearchWorkflow(ResearchWorkflow):
    """
    Main ResearchForge workflow.

    1. Decide whether search is required.
    2. Perform search (if needed).
    3. Rank search results.
    4. Build prompt.
    5. Invoke LLM.
    """

    def __init__(
        self,
        llm_service: LLMService,
        prompt_builder: PromptBuilder,
        search_service: SearchService,
        search_ranking_service: SearchRankingService,
        router: ResearchRouter,
        context_formatter: SearchContextFormatter,
    ) -> None:

        self._llm_service = llm_service
        self._prompt_builder = prompt_builder
        self._search_service = search_service
        self._search_ranking_service = search_ranking_service
        self._router = router
        self._context_formatter = context_formatter

    async def run(
    self,
    state: ResearchState,
) -> ResearchState:

        state.strategy = await self._router.route(
            state,
        )

        if state.strategy == ResearchStrategy.WEB_SEARCH:

            query = state.messages[-1].content

            search_request = SearchRequest(
                query=query,
                max_results=3,
            )

            state.search_results = await self._search_service.search(
                search_request,
            )

            state.search_results = await self._search_ranking_service.rank(
                search_request,
                state.search_results,
            )

            state.context = self._context_formatter.format(
            state.search_results,
            )

        prompt = self._prompt_builder.build(
            messages=state.messages,
            context=state.context,
        )

        state.response = await self._llm_service.invoke(
            LLMRequest(
                messages=prompt,
            )
        )

        return state