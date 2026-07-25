from __future__ import annotations

from abc import ABC, abstractmethod

from backend.app.ai.search.models import SearchResult


class SearchRanker(ABC):
    """
    Base interface for all search rankers.
    """

    @abstractmethod
    async def rank(
        self,
        query: str,
        results: list[SearchResult],
    ) -> list[SearchResult]:
        """
        Return the ranked search results.
        """
        raise NotImplementedError