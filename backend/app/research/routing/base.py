from __future__ import annotations

from abc import ABC, abstractmethod

from backend.app.research.models import ResearchStrategy
from backend.app.research.engine import ResearchState


class ResearchRouter(ABC):
    """
    Determines how a request should be executed.
    """

    @abstractmethod
    async def route(
        self,
        state: ResearchState,
    ) -> ResearchStrategy:
        raise NotImplementedError