from __future__ import annotations

from abc import ABC, abstractmethod

from backend.app.research.cache.models import ResearchCacheEntry


class ResearchCacheRepository(ABC):

    @abstractmethod
    async def find(
        self,
        question: str,
    ) -> ResearchCacheEntry | None:
        ...

    @abstractmethod
    async def save(
        self,
        entry: ResearchCacheEntry,
    ) -> None:
        ...

    @abstractmethod
    async def all(
        self,
    ) -> list[ResearchCacheEntry]:
        ...