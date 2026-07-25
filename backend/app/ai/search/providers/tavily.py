from __future__ import annotations

from tavily import AsyncTavilyClient

from backend.app.ai.search.interfaces import BaseSearchProvider
from backend.app.ai.search.models import (
    SearchRequest,
    SearchResponse,
    SearchResult,
)

from urllib.parse import urlparse
class TavilyProvider(BaseSearchProvider):
    """
    Tavily search provider.
    """

    def __init__(
        self,
        client: AsyncTavilyClient,
    ) -> None:
        self._client = client

    async def search(
        self,
        request: SearchRequest,
    ) -> SearchResponse:

        response = await self._client.search(
            query=request.query,
            max_results=request.max_results,
        )

        results = [
            SearchResult(
                title=result["title"],
                url=result["url"],
                content=result["content"],
                    source=urlparse(result["url"]).netloc.replace("www.", ""),

            )
            for result in response["results"]
        ]

        return SearchResponse(
            results=results,
        )