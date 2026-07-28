from __future__ import annotations

from pydantic import BaseModel

from backend.app.ai.llms.models import (
    LLMResponse,
    Message,
)

from backend.app.ai.search.models import SearchResponse
from backend.app.research.memory.models import ConversationMemory
from backend.app.research.summary import ConversationSummary
class ResearchState(BaseModel):
    """
    Shared state passed through the research workflow.
    """

    messages: list[Message]

    strategy: str | None = None

    search_results: SearchResponse | None = None

    context: str = ""

    response: LLMResponse | None = None
    memory: ConversationMemory | None = None
    summary: ConversationSummary | None = None