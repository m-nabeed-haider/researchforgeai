from __future__ import annotations

from pydantic import BaseModel

from backend.app.ai.llms.models import (
    LLMResponse,
    Message,
)
from backend.app.ai.search.models import SearchResponse


class ResearchState(BaseModel):
    """
    Shared mutable state for the research workflow.
    """

    messages: list[Message]

    search_results: SearchResponse | None = None

    context: str | None = None

    response: LLMResponse | None = None