from __future__ import annotations

import time
from typing import Any

from groq import AsyncGroq
from groq import AuthenticationError as GroqAuthenticationError
from groq import RateLimitError as GroqRateLimitError

from backend.app.ai.llms.exceptions import (
    AuthenticationError,
    LLMProviderError,
    RateLimitError,
)
from backend.app.ai.llms.interfaces import BaseLLMProvider
from backend.app.ai.llms.models import (
    FinishReason,
    LLMProviderType,
    LLMRequest,
    LLMResponse,
    Message,
    TokenUsage,
)


class GroqProvider(BaseLLMProvider):
    """
    Groq implementation of the provider interface.
    """

    def __init__(
        self,
        client: AsyncGroq,
        model: str,
    ) -> None:
        self._client = client
        self._model = model

    def _to_groq_messages(
        self,
        messages: list[Message],
    ) -> list[dict[str, Any]]:
        """
        Convert provider-agnostic messages into
        Groq/OpenAI compatible chat messages.
        """

        return [
            {
                "role": message.role.value,
                "content": message.content,
            }
            for message in messages
        ]

    async def invoke(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        """
        Execute a completion request against Groq.
        """

        sdk_messages = self._to_groq_messages(request.messages)

        start_time = time.perf_counter()

        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=sdk_messages,
                temperature=request.temperature,
                max_completion_tokens=request.max_tokens,
            )

        except GroqAuthenticationError as exc:
            raise AuthenticationError("Groq authentication failed.") from exc

        except GroqRateLimitError as exc:
            raise RateLimitError("Groq rate limit exceeded.") from exc

        except Exception as exc:
            raise LLMProviderError(f"Groq provider error: {exc}") from exc

        latency_ms = (time.perf_counter() - start_time) * 1000

        choice = response.choices[0]

        usage = None

        if response.usage:
            usage = TokenUsage(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
            )

        finish_reason = None

        if choice.finish_reason:
            try:
                finish_reason = FinishReason(choice.finish_reason)
            except ValueError:
                finish_reason = FinishReason.STOP

        return LLMResponse(
            content=choice.message.content or "",
            model=response.model,
            provider=LLMProviderType.GROQ,
            finish_reason=finish_reason,
            usage=usage,
            latency_ms=latency_ms,
            cached=False,
        )
