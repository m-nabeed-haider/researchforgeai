from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class MemoryMessage:
    role: str
    content: str


@dataclass(slots=True)
class ConversationMemory:
    """
    Stores the complete conversation history for a session.
    """

    session_id: str
    messages: list[MemoryMessage] = field(default_factory=list)