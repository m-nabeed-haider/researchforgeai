from __future__ import annotations

from backend.app.research.memory.models import (
    ConversationMemory,
    MemoryMessage,
)
from backend.app.research.memory.repository import MemoryRepository


class MemoryService:

    def __init__(
        self,
        repository: MemoryRepository,
    ) -> None:
        self._repository = repository

    async def load(
        self,
        session_id: str,
    ) -> ConversationMemory:

        return await self._repository.get(
            session_id,
        )

    async def save(
        self,
        memory: ConversationMemory,
    ) -> None:

        await self._repository.save(
            memory,
        )

    async def append(
        self,
        session_id: str,
        role: str,
        content: str,
    ) -> ConversationMemory:

        memory = await self._repository.get(
            session_id,
        )

        memory.messages.append(
            MemoryMessage(
                role=role,
                content=content,
            )
        )

        await self._repository.save(
            memory,
        )

        return memory