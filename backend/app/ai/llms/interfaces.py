from __future__ import annotations

from abc import ABC, abstractmethod

from backend.app.ai.llms.models import LLMRequest, LLMResponse


class BaseLLMProvider(ABC):
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
