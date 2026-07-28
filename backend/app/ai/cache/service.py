from __future__ import annotations

from datetime import datetime

from backend.app.ai.cache.hashing import PromptHasher
from backend.app.ai.cache.models import CachedPrompt
from backend.app.ai.cache.repository import PromptCacheRepository
from backend.app.ai.llms.models import Message


class PromptCacheService:

    def __init__(
        self,
        repository: PromptCacheRepository,
    ) -> None:

        self._repository = repository

    async def get_or_create(
        self,
        prefix: list[Message],
    ) -> list[Message]:

        cache_key = PromptHasher.hash_messages(
            prefix,
        )

        entry = await self._repository.get(
            cache_key,
        )

        if entry is not None:

            print("=" * 50)
            print("PREFIX CACHE HIT")
            print("=" * 50)

            return entry.messages

        print("=" * 50)
        print("PREFIX CACHE MISS")
        print("=" * 50)

        entry = CachedPrompt(
            key=cache_key,
            messages=prefix,
            created_at=datetime.utcnow(),
        )

        await self._repository.save(
            entry,
        )

        return prefix