from __future__ import annotations

from backend.app.ai.search.models import SearchResult

from backend.app.ai.search.ranking.base import SearchRanker


class IdentitySearchRanker(SearchRanker):
    """
    Leaves search results unchanged.
    """

    async def rank(
        self,
        query: str,
        results: list[SearchResult],
    ) -> list[SearchResult]:

        return results