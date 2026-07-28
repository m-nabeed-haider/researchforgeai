from backend.app.ai.cache.models import CachedPrompt
from backend.app.ai.cache.repository import PromptCacheRepository


class InMemoryPromptCacheRepository(PromptCacheRepository):

    def __init__(self) -> None:

        self._store: dict[str, CachedPrompt] = {}

    async def get(
        self,
        key: str,
    ) -> CachedPrompt | None:

        return self._store.get(key)

    async def save(
        self,
        prompt: CachedPrompt,
    ) -> None:

        self._store[prompt.key] = prompt