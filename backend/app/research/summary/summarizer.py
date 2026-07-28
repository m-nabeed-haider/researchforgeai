from __future__ import annotations

from backend.app.ai.llms.models import (
    LLMRequest,
    Message,
    MessageRole,
)
from backend.app.ai.llms.service import LLMService

from backend.app.research.summary.prompts import SUMMARY_SYSTEM_PROMPT


class ConversationSummarizer:

    def __init__(
        self,
        llm_service: LLMService,
    ) -> None:

        self._llm = llm_service

    async def summarize(
        self,
        previous_summary: str,
        messages: list[Message],
    ) -> str:

        conversation = "\n".join(
            f"{message.role}: {message.content}"
            for message in messages
        )

        prompt = [
            Message(
                role=MessageRole.SYSTEM,
                content=SUMMARY_SYSTEM_PROMPT,
            ),
            Message(
                role=MessageRole.USER,
                content=(
                    f"Previous Summary:\n"
                    f"{previous_summary}\n\n"
                    f"Latest Conversation:\n"
                    f"{conversation}"
                ),
            ),
        ]

        response = await self._llm.invoke(
            LLMRequest(
                messages=prompt,
            )
        )

        return response.content.strip()