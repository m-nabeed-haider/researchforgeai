from pydantic import BaseModel

from backend.app.ai.llms.models import Message


class ChatRequest(BaseModel):
    messages: list[Message]


class ChatSource(BaseModel):
    name: str
    url: str


class ChatResponse(BaseModel):
    response: str
    sources: list[ChatSource] = []