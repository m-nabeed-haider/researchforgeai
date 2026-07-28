from __future__ import annotations

from pydantic import BaseModel


class ConversationSummary(BaseModel):
    session_id: str
    summary: str = ""