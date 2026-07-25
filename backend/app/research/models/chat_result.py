from __future__ import annotations

from pydantic import BaseModel

from backend.app.ai.llms.models import LLMResponse
from backend.app.ai.search.models import SearchResult


class ChatResult(BaseModel):
    """
    Application-level chat response.

    Keeps API layer independent from workflow internals.
    """

    response: LLMResponse

    sources: list[SearchResult]