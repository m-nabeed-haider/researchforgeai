from __future__ import annotations

from backend.app.research.summary.models import ConversationSummary
from backend.app.research.summary.repository import SummaryRepository


class InMemorySummaryRepository(SummaryRepository):

    def __init__(self) -> None:
        self._store: dict[str, ConversationSummary] = {}

    async def get(
        self,
        session_id: str,
    ) -> ConversationSummary:

        if session_id not in self._store:
            self._store[session_id] = ConversationSummary(
                session_id=session_id,
            )

        return self._store[session_id]

    async def save(
        self,
        summary: ConversationSummary,
    ) -> None:

        self._store[summary.session_id] = summary