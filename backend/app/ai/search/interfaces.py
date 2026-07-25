from __future__ import annotations

from abc import ABC, abstractmethod

from backend.app.ai.search.models import (
    SearchRequest,
    SearchResponse,
)


class BaseSearchProvider(ABC):
    """
    Base interface for all search providers.
    """

    @abstractmethod
    async def search(
        self,
        request: SearchRequest,
    ) -> SearchResponse:
        raise NotImplementedError