from __future__ import annotations

from backend.app.ai.search.interfaces import BaseSearchProvider
from backend.app.ai.search.models import (
    SearchRequest,
    SearchResponse,
)


class SearchService:
    """
    Facade over the configured search provider.

    Future responsibilities:

    - caching
    - retries
    - metrics
    - observability
    """

    def __init__(
        self,
        provider: BaseSearchProvider,
    ) -> None:
        self._provider = provider

    async def search(
        self,
        request: SearchRequest,
    ) -> SearchResponse:

        return await self._provider.search(request)