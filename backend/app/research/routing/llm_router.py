from __future__ import annotations

from pathlib import Path

from backend.app.ai.llms.models import (
    LLMRequest,
    Message,
    MessageRole,
)
from backend.app.ai.llms.service import LLMService

from backend.app.research.routing.base import ResearchRouter
from backend.app.research.models import ResearchStrategy
from backend.app.research.engine import ResearchState


class LLMResearchRouter(ResearchRouter):
    """
    Uses the LLM to decide whether external research is required.
    """

    def __init__(
        self,
        llm_service: LLMService,
        prompt_path: Path,
    ) -> None:

        self._llm_service = llm_service

        self._system_prompt = prompt_path.read_text(
            encoding="utf-8",
        ).strip()

    async def route(
        self,
        state: ResearchState,
    ) -> ResearchStrategy:

        latest_message = state.messages[-1].content

        summary = "None"

        if (
            state.summary is not None
            and state.summary.summary
        ):
            summary = state.summary.summary

        routing_input = f"""
Conversation Summary
====================

{summary}

Latest User Message
===================

{latest_message}
""".strip()

        # Debug (remove later)
        print("=" * 80)
        print("ROUTER INPUT")
        print(routing_input)
        print("=" * 80)

        response = await self._llm_service.invoke(
            LLMRequest(
                messages=[
                    Message(
                        role=MessageRole.SYSTEM,
                        content=self._system_prompt,
                    ),
                    Message(
                        role=MessageRole.USER,
                        content=routing_input,
                    ),
                ],
                temperature=0.0,
                max_tokens=5,
            )
        )

        decision = response.content.strip().upper()

        print(f"ROUTER DECISION: {decision}")

        if "WEB_SEARCH" in decision:
            return ResearchStrategy.WEB_SEARCH

        return ResearchStrategy.DIRECT_LLM