from __future__ import annotations

from groq import AsyncGroq

from backend.app.ai.llms.providers.groq import GroqProvider
from backend.app.ai.llms.service import LLMService
from backend.app.core.config.settings import Settings, get_settings
from backend.app.research.services.chat_service import ChatService

class Container:
    """
    Application dependency container.

    Responsible for constructing application services
    and their dependencies.
    """

    def __init__(self) -> None:
        self._settings: Settings | None = None
        self._groq_client: AsyncGroq | None = None
        self._groq_provider: GroqProvider | None = None
        self._llm_service: LLMService | None = None
        self._chat_service: ChatService | None = None
    @property
    def settings(self) -> Settings:
        if self._settings is None:
            self._settings = get_settings()

        return self._settings

    @property
    def groq_client(self) -> AsyncGroq:
        if self._groq_client is None:
            self._groq_client = AsyncGroq(
                api_key=self.settings.groq_api_key
            )

        return self._groq_client

    @property
    def groq_provider(self) -> GroqProvider:
        if self._groq_provider is None:
            self._groq_provider = GroqProvider(
                client=self.groq_client,
                model=self.settings.llm_model,
            )

        return self._groq_provider

    @property
    def llm_service(self) -> LLMService:
        if self._llm_service is None:
            self._llm_service = LLMService(
                provider=self.groq_provider
            )

        return self._llm_service
    @property
    def chat_service(self) -> ChatService:
        if self._chat_service is None:
            self._chat_service = ChatService(
                llm_service=self.llm_service
            )

        return self._chat_service