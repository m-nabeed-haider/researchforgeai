from __future__ import annotations

from groq import AsyncGroq

from backend.app.ai.llms.providers.groq import GroqProvider
from backend.app.ai.llms.service import LLMService

from backend.app.core.config.settings import (
    Settings,
    get_settings,
)
from backend.app.research.routing import (
    LLMResearchRouter,
)

from backend.app.research.services.chat_service import ChatService
from backend.app.research.workflows.simple_workflow import (
    SimpleResearchWorkflow,
)
from pathlib import Path

from backend.app.ai.prompts import PromptBuilder
from tavily import AsyncTavilyClient

from backend.app.ai.search import SearchService
from backend.app.ai.search.providers import TavilyProvider
class Container:
    """
    Application dependency container.

    Responsible for constructing and managing
    application-wide singleton dependencies.
    """

    def __init__(self) -> None:
        self._settings: Settings | None = None

        self._groq_client: AsyncGroq | None = None
        self._groq_provider: GroqProvider | None = None

        self._llm_service: LLMService | None = None

        self._research_workflow: SimpleResearchWorkflow | None = None

        self._chat_service: ChatService | None = None
        self._prompt_builder: PromptBuilder | None = None
        self._tavily_provider: TavilyProvider | None = None
        self._search_service: SearchService | None = None
        self._router: LLMResearchRouter | None = None
    @property
    def settings(self) -> Settings:
        if self._settings is None:
            self._settings = get_settings()

        return self._settings

    @property
    def groq_client(self) -> AsyncGroq:
        if self._groq_client is None:
            self._groq_client = AsyncGroq(
                api_key=self.settings.groq_api_key,
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
                provider=self.groq_provider,
            )

        return self._llm_service

    @property
    def research_workflow(self) -> SimpleResearchWorkflow:
        if self._research_workflow is None:
            self._research_workflow = SimpleResearchWorkflow(
                llm_service=self.llm_service,
                prompt_builder=self.prompt_builder,
                search_service=self.search_service,
                router=self.router,
            )

        return self._research_workflow

    @property
    def chat_service(self) -> ChatService:
        if self._chat_service is None:
            self._chat_service = ChatService(
                workflow=self.research_workflow,
            )

        return self._chat_service
    @property
    def prompt_builder(self) -> PromptBuilder:

        if self._prompt_builder is None:

            self._prompt_builder = PromptBuilder(
                Path("backend/app/ai/prompts/system.md"),
            )

        return self._prompt_builder
    @property
    def tavily_provider(self) -> TavilyProvider:

        if self._tavily_provider is None:

            client = AsyncTavilyClient(
                api_key=self.settings.tavily_api_key,
            )

            self._tavily_provider = TavilyProvider(
                client=client,
            )

        return self._tavily_provider
    @property
    def search_service(self) -> SearchService:

        if self._search_service is None:

            self._search_service = SearchService(
                provider=self.tavily_provider,
            )

        return self._search_service
    @property
    def router(self) -> LLMResearchRouter:

        if self._router is None:

            self._router = LLMResearchRouter(
                llm_service=self.llm_service,
                prompt_path=Path(
                    "backend/app/research/routing/prompt.md",
                ),
            )

        return self._router