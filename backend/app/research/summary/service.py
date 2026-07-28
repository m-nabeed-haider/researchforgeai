from __future__ import annotations

from backend.app.research.summary.models import ConversationSummary
from backend.app.research.summary.repository import SummaryRepository


class SummaryService:

    def __init__(
        self,
        repository: SummaryRepository,
    ) -> None:
        self._repository = repository

    async def load(
        self,
        session_id: str,
    ) -> ConversationSummary:

        return await self._repository.get(session_id)

    async def save(
        self,
        summary: ConversationSummary,
    ) -> None:

        await self._repository.save(summary)