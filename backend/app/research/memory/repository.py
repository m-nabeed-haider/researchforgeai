from __future__ import annotations

from abc import ABC, abstractmethod

from backend.app.research.memory.models import ConversationMemory


class MemoryRepository(ABC):

    @abstractmethod
    async def get(
        self,
        session_id: str,
    ) -> ConversationMemory:
        ...

    @abstractmethod
    async def save(
        self,
        memory: ConversationMemory,
    ) -> None:
        ...