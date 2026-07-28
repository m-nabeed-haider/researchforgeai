from __future__ import annotations

from backend.app.ai.llms.models import Message
from backend.app.research.engine import ResearchState
from backend.app.research.engine import ResearchWorkflow
from backend.app.research.models import ChatResult
from backend.app.research.memory import MemoryService
from backend.app.research.summary import (
    SummaryService,
    ConversationSummarizer,
)

MAX_MEMORY_MESSAGES = 10
KEEP_RECENT_MESSAGES = 4


class ChatService:
    """
    Coordinates chat requests.
    """

    def __init__(
        self,
        workflow: ResearchWorkflow,
        memory_service: MemoryService,
        summary_service: SummaryService,
        summarizer: ConversationSummarizer,
    ) -> None:

        self._workflow = workflow
        self._memory_service = memory_service
        self._summary_service = summary_service
        self._summarizer = summarizer

    async def chat(
        self,
        session_id: str,
        messages: list[Message],
    ) -> ChatResult:

        # Load conversation state
        memory = await self._memory_service.load(
            session_id=session_id,
        )

        summary = await self._summary_service.load(
            session_id=session_id,
        )
        print("=" * 60)
        print("Loaded Summary:")
        print(repr(summary.summary))
        print("=" * 60)
        # Build workflow state
        state = ResearchState(
            messages=messages,
            memory=memory,
            summary=summary,
        )

        # Generate assistant response
        state = await self._workflow.run(
            state,
        )

        # Persist latest user turn
        latest_user = messages[-1]

        await self._memory_service.append(
            session_id=session_id,
            role="user",
            content=latest_user.content,
        )

        # Persist assistant turn
        await self._memory_service.append(
            session_id=session_id,
            role="assistant",
            content=state.response.content,
        )

        # Reload memory after appending
        memory = await self._memory_service.load(
            session_id=session_id,
        )

        # Summarize only when memory exceeds the limit
        if len(memory.messages) > MAX_MEMORY_MESSAGES:

            old_messages = memory.messages[:-KEEP_RECENT_MESSAGES]

            recent_messages = memory.messages[-KEEP_RECENT_MESSAGES:]

            updated_summary = await self._summarizer.summarize(
                previous_summary=summary.summary,
                messages=old_messages,
            )

            summary.summary = updated_summary
            print("=" * 50)
            print("Upated Summary")
            print(updated_summary)
            print("=" * 50)
            await self._summary_service.save(
                summary,
            )

            memory.messages = recent_messages

            await self._memory_service.save(
                memory,
            )
            #print(memory.messages)

        sources = []

        if state.search_results is not None:
            sources = state.search_results.results

        return ChatResult(
            response=state.response,
            sources=sources,
        )