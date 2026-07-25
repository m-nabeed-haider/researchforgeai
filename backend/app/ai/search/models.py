from __future__ import annotations

from pydantic import BaseModel


class SearchResult(BaseModel):
    """
    A single search result.
    """

    title: str
    url: str
    content: str
    source: str

class SearchRequest(BaseModel):
    """
    Provider-agnostic search request.
    """

    query: str
    max_results: int = 5


class SearchResponse(BaseModel):
    """
    Provider-agnostic search response.
    """

    results: list[SearchResult]