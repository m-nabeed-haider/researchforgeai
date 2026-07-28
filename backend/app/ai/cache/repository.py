from abc import ABC, abstractmethod

from backend.app.ai.cache.models import CachedPrompt


class PromptCacheRepository(ABC):

    @abstractmethod
    async def get(
        self,
        key: str,
    ) -> CachedPrompt | None:
        ...

    @abstractmethod
    async def save(
        self,
        prompt: CachedPrompt,
    ) -> None:
        ...