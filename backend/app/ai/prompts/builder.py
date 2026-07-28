from __future__ import annotations

from backend.app.ai.llms.models import Message
from backend.app.ai.prompts.prefix_builder import PrefixBuilder
from backend.app.ai.prompts.suffix_builder import SuffixBuilder
from backend.app.ai.cache.service import PromptCacheService


class PromptBuilder:
    """
    Orchestrates prompt construction.

    - Builds the cacheable prefix.
    - Retrieves/stores it in the prompt cache.
    - Builds the dynamic suffix.
    """

    def __init__(
        self,
        prefix_builder: PrefixBuilder,
        suffix_builder: SuffixBuilder,
        prompt_cache: PromptCacheService,
    ) -> None:

        self._prefix_builder = prefix_builder
        self._suffix_builder = suffix_builder
        self._prompt_cache = prompt_cache

    async def build(
        self,
        messages: list[Message],
        context: str | None = None,
        summary: str = "",
    ) -> list[Message]:

        prefix = self._prefix_builder.build(
            summary=summary,
            context=context,
        )

        prefix = await self._prompt_cache.get_or_create(
            prefix,
        )

        
        suffix = self._suffix_builder.build(
            messages,
        )

        return prefix + suffix