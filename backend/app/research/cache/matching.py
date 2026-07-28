from __future__ import annotations

import re

from backend.app.research.cache.models import (
    ResearchCacheEntry,
)


class ResearchCacheMatcher:
    """
    Responsible for matching user questions against
    cached research entries.
    """

    def find_best_match(
        self,
        question: str,
        entries: list[ResearchCacheEntry],
    ) -> ResearchCacheEntry | None:

        normalized_question = self._normalize(
            question,
        )

        for entry in entries:

            if (
                self._normalize(entry.question)
                == normalized_question
            ):
                return entry

        return None

    @staticmethod
    def _normalize(
        text: str,
    ) -> str:
        """
        Normalize text before matching.

        Example:
            " What is LangGraph? "
            ->
            "what is langgraph"
        """

        text = text.lower().strip()

        text = re.sub(
            r"[^\w\s]",
            "",
            text,
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text