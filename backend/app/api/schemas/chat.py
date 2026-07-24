from pydantic import BaseModel

from backend.app.ai.llms.models import Message


class ChatRequest(BaseModel):
    messages: list[Message]


class ChatResponse(BaseModel):
    response: str