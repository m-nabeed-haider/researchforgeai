from __future__ import annotations

from abc import ABC, abstractmethod

from backend.app.ai.llms.models import LLMResponse
from backend.app.research.models.research_request import ResearchRequest


class ResearchWorkflow(ABC):
    """
    Base interface for all research workflows.
    """

    @abstractmethod
    async def run(
        self,
        request: ResearchRequest,
    ) -> LLMResponse:
        """
        Execute the workflow.
        """
        raise NotImplementedError