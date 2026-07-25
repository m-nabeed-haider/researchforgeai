from __future__ import annotations

from backend.app.ai.search.models import (
    SearchRequest,
    SearchResponse,
)

from backend.app.ai.search.ranking.base import SearchRanker


class SearchRankingService:
    """
    Coordinates search result ranking.
    """

    def __init__(
        self,
        ranker: SearchRanker,
    ) -> None:

        self._ranker = ranker

    async def rank(
        self,
        request: SearchRequest,
        response: SearchResponse,
    ) -> SearchResponse:

        ranked_results = await self._ranker.rank(
            query=request.query,
            results=response.results,
        )

        return SearchResponse(
            results=ranked_results,
        )