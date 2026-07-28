from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from backend.app.ai.search.models import SearchResponse


class ResearchCacheEntry(BaseModel):
    question: str
    formatted_context: str
    search_response: SearchResponse
    created_at: datetime