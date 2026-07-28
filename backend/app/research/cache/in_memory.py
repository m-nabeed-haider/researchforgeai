from __future__ import annotations

from backend.app.research.cache.models import ResearchCacheEntry
from backend.app.research.cache.repository import (
    ResearchCacheRepository,
)


class InMemoryResearchCacheRepository(
    ResearchCacheRepository,
):

    def __init__(self) -> None:
        self._entries: list[ResearchCacheEntry] = []

    async def find(
        self,
        question: str,
    ) -> ResearchCacheEntry | None:

        for entry in self._entries:
            if entry.question == question:
                return entry

        return None

    async def save(
        self,
        entry: ResearchCacheEntry,
    ) -> None:

        self._entries.append(entry)

    async def all(
        self,
    ) -> list[ResearchCacheEntry]:

        return self._entries