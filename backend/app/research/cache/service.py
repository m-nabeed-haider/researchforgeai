from __future__ import annotations

from datetime import datetime

from backend.app.ai.search.models import SearchResponse

from backend.app.research.cache.matching import (
    ResearchCacheMatcher,
)
from backend.app.research.cache.models import (
    ResearchCacheEntry,
)
from backend.app.research.cache.repository import (
    ResearchCacheRepository,
)


class ResearchCacheService:

    def __init__(
        self,
        repository: ResearchCacheRepository,
        matcher: ResearchCacheMatcher,
    ) -> None:

        self._repository = repository
        self._matcher = matcher

    async def get(
        self,
        question: str,
    ) -> ResearchCacheEntry | None:

        entries = await self._repository.all()

        return self._matcher.find_best_match(
            question=question,
            entries=entries,
        )

    async def save(
    self,
    question: str,
    formatted_context: str,
    search_response: SearchResponse,
) -> None:

        entry = ResearchCacheEntry(
            question=question,
            formatted_context=formatted_context,
            search_response=search_response,
            created_at=datetime.utcnow(),
        )

        await self._repository.save(entry)