from __future__ import annotations

from pathlib import Path

from backend.app.ai.llms.models import (
    Message,
    MessageRole,
)


class PromptBuilder:
    """
    Builds the final prompt sent to the LLM.
    """

    def __init__(
        self,
        system_prompt_path: Path,
    ) -> None:

        self._system_prompt = system_prompt_path.read_text(
            encoding="utf-8",
        ).strip()

    def build(
        self,
        conversation: list[Message],
        context: str | None = None,
    ) -> list[Message]:

        messages = [
            Message(
                role=MessageRole.SYSTEM,
                content=self._system_prompt,
            )
        ]

        if context:

            messages.append(
                Message(
                    role=MessageRole.SYSTEM,
                    content=(
                        "Research Context\n"
                        "================\n\n"
                        f"{context}\n\n"
                        "Instructions:\n"
                        "- Prefer the supplied sources when answering.\n"
                        "- If the sources are insufficient, say so.\n"
                        "- Do not fabricate information.\n"
                        "- Keep the answer concise."
                    ),
                )
            )

        messages.extend(conversation)

        return messages