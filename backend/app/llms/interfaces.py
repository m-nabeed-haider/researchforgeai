from __future__ import annotations

from abc import ABC, abstractmethod

from backend.app.llms.models import LLMRequest, LLMResponse


class LLMProvider(ABC):
    """
    Interface implemented by every LLM provider.
    """

    @abstractmethod
    async def invoke(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        """
        Execute an LLM request.
        """
        raise NotImplementedError