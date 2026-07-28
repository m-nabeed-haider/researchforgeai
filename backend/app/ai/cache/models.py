from __future__ import annotations

from datetime import datetime

from backend.app.ai.llms.models import Message


class CachedPrompt:

    def __init__(
        self,
        key: str,
        messages: list[Message],
        created_at: datetime,
    ) -> None:

        self.key = key
        self.messages = messages
        self.created_at = created_at