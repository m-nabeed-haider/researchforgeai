from __future__ import annotations

from backend.app.ai.llms.models import Message


class SuffixBuilder:
    """
    Builds the dynamic portion of the prompt.

    This portion changes every request and therefore
    should never be cached.
    """

    def build(
        self,
        messages: list[Message],
    ) -> list[Message]:

        return list(messages)