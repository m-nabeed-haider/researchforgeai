from __future__ import annotations

from backend.app.research.routing.base import ResearchRouter
from backend.app.research.models import ResearchStrategy
from backend.app.research.engine import ResearchState


SEARCH_KEYWORDS = {
    "latest",
    "today",
    "recent",
    "current",
    "news",
    "breaking",
    "2025",
    "2026",
}


class SimpleResearchRouter(ResearchRouter):
    """
    Simple keyword-based router.
    """

    async def route(
        self,
        state: ResearchState,
    ) -> ResearchStrategy:

        query = state.messages[-1].content.lower()

        if any(
            keyword in query
            for keyword in SEARCH_KEYWORDS
        ):
            return ResearchStrategy.WEB_SEARCH

        return ResearchStrategy.DIRECT_LLM