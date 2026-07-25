from __future__ import annotations

from backend.app.ai.search.models import SearchResult
from backend.app.ai.search.ranking.base import SearchRanker
from backend.app.core.http import HttpClient


class JinaSearchRanker(SearchRanker):
    """
    Jina AI reranker.
    """

    def __init__(
        self,
        client: HttpClient,
        api_key: str,
        base_url: str,
        model: str,
    ) -> None:

        self._client = client
        self._api_key = api_key
        self._base_url = base_url
        self._model = model

    async def rank(
        self,
        query: str,
        results: list[SearchResult],
    ) -> list[SearchResult]:

        if len(results) <= 1:
            return results

        response = await self._client.post(
            f"{self._base_url}/rerank",
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self._model,
                "query": query,
                "documents": [
                    result.content
                    for result in results
                ],
                "top_n": len(results),
                "return_documents": False,
            },
        )

        payload = response.json()

        ranked: list[SearchResult] = []

        for item in payload["results"]:
            ranked.append(
                results[item["index"]]
            )

        return ranked