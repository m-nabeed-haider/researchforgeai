from pydantic import BaseModel

from backend.app.ai.llms.models import Message


class ChatRequest(BaseModel):
    session_id: str
    message: Message


class ChatSource(BaseModel):
    name: str
    url: str


class ChatResponse(BaseModel):
    response: str
    sources: list[ChatSource] = []