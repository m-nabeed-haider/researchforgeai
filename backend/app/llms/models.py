from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class ResponseFormat(str, Enum):
    TEXT = "text"
    JSON = "json"
    MARKDOWN = "markdown"


class FinishReason(str, Enum):
    STOP = "stop"
    LENGTH = "length"
    TOOL_CALL = "tool_call"
    CONTENT_FILTER = "content_filter"


class LLMProviderType(str, Enum):
    OPENAI = "openai"
    GEMINI = "gemini"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"


class Message(BaseModel):
    role: MessageRole
    content: str

    name: str | None = None

    metadata: dict[str, object] = Field(default_factory=dict)


class LLMRequest(BaseModel):
    """
    Provider-agnostic request model.
    """

    messages: list[Message]

    temperature: float = 0.0

    max_tokens: int | None = None

    stream: bool = False

    response_format: ResponseFormat = ResponseFormat.TEXT

    tools: list[dict] = Field(default_factory=list)

    images: list[str] = Field(default_factory=list)

    documents: list[str] = Field(default_factory=list)


class TokenUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class LLMResponse(BaseModel):
    """
    Unified response returned by every provider.
    """

    content: str

    model: str

    provider: LLMProviderType

    finish_reason: FinishReason | None = None

    usage: TokenUsage | None = None

    latency_ms: float | None = None

    cached: bool = False