from __future__ import annotations

from abc import ABC, abstractmethod

from backend.app.research.summary.models import ConversationSummary


class SummaryRepository(ABC):

    @abstractmethod
    async def get(
        self,
        session_id: str,
    ) -> ConversationSummary:
        ...

    @abstractmethod
    async def save(
        self,
        summary: ConversationSummary,
    ) -> None:
        ...