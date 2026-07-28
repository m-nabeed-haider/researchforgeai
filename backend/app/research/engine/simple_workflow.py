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
from backend.app.ai.llms.models import Message
from backend.app.research.cache import ResearchCacheService
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
        cache_service: ResearchCacheService,

    ) -> None:

        self._llm_service = llm_service
        self._prompt_builder = prompt_builder
        self._search_service = search_service
        self._search_ranking_service = search_ranking_service
        self._router = router
        self._context_formatter = context_formatter
        self._cache_service = cache_service
        
    async def run(
    self,
    state: ResearchState,
) -> ResearchState:
        
        query = state.messages[-1].content

        cached = await self._cache_service.get(
            question=query,
        )

        if cached is not None:

            state.context = cached.formatted_context

            state.search_results = cached.search_response
            
        if cached is None:    
            state.strategy = await self._router.route(
                state,
            )
        else:
            state.strategy = ResearchStrategy.DIRECT_LLM
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
            await self._cache_service.save(
                question=query,
                formatted_context=state.context,
                search_response=state.search_results,
            )
        conversation = []

        if state.memory is not None:
            conversation.extend(
                Message(
                    role=message.role,
                    content=message.content,
                )
                for message in state.memory.messages
            )

        conversation.extend(state.messages)
        summary = ""

        if state.summary is not None:
            summary = state.summary.summary
        prompt = await self._prompt_builder.build(
            messages=conversation,
            context=state.context,
            summary=summary,
        )
        
        
        state.response = await self._llm_service.invoke(
            LLMRequest(
                messages=prompt,
            )
        )

        return state