from __future__ import annotations

from backend.app.research.memory.models import ConversationMemory
from backend.app.research.memory.repository import MemoryRepository


class InMemoryMemoryRepository(MemoryRepository):
    """
    Simple in-memory repository.

    Stores conversation history in a dictionary keyed
    by session_id.
    """

    def __init__(self) -> None:
        self._store: dict[str, ConversationMemory] = {}

    async def get(
        self,
        session_id: str,
    ) -> ConversationMemory:

        if session_id not in self._store:
            self._store[session_id] = ConversationMemory(
                session_id=session_id,
            )

        return self._store[session_id]

    async def save(
        self,
        memory: ConversationMemory,
    ) -> None:

        self._store[memory.session_id] = memory