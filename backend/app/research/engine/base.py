from __future__ import annotations

from abc import ABC, abstractmethod

from backend.app.research.engine import ResearchState


class ResearchWorkflow(ABC):
    """
    Base interface for all research workflows.
    """

    @abstractmethod
    async def run(
        self,
        state: ResearchState,
    ) -> ResearchState:
        """
        Execute the workflow.
        """
        raise NotImplementedError