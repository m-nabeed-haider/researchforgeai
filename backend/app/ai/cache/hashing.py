from __future__ import annotations

import hashlib
import json

from backend.app.ai.llms.models import Message


class PromptHasher:

    @staticmethod
    def hash_messages(
        messages: list[Message],
    ) -> str:

        payload = [
            {
                "role": message.role.value,
                "content": message.content,
            }
            for message in messages
        ]

        serialized = json.dumps(
            payload,
            sort_keys=True,
            ensure_ascii=False,
        )

        return hashlib.sha256(
            serialized.encode("utf-8"),
        ).hexdigest()