from pathlib import Path

import httpx
from groq import AsyncGroq
from tavily import AsyncTavilyClient

from backend.app.ai.llms.providers.groq import GroqProvider
from backend.app.ai.llms.service import LLMService
from backend.app.ai.prompts import PromptBuilder,PrefixBuilder,SuffixBuilder
from backend.app.ai.search import SearchService
from backend.app.ai.search.providers import TavilyProvider
from backend.app.ai.search.ranking import (
    JinaSearchRanker,
    SearchRanker,
    SearchRankingService,
)
from backend.app.core.config.settings import (
    Settings,
    get_settings,
)
from backend.app.core.http import HttpClient
from backend.app.research.routing import LLMResearchRouter
from backend.app.services.chat_service import ChatService
from backend.app.research.engine.simple_workflow import (
    SimpleResearchWorkflow,
)
from backend.app.ai.search.formatting import (
    SearchContextFormatter,
)
from backend.app.research.memory import (
    InMemoryMemoryRepository,
    MemoryService,
)
from backend.app.research.cache import (
    InMemoryResearchCacheRepository,
    ResearchCacheMatcher,
    ResearchCacheService,
)
from backend.app.ai.cache import InMemoryPromptCacheRepository,PromptCacheService
from backend.app.research.summary import InMemorySummaryRepository,SummaryService,ConversationSummarizer
class Container:
    """
    Application dependency container.

    Provides lazy singleton construction for
    application-wide dependencies.
    """

    def __init__(self) -> None:

        # Configuration
        self._settings: Settings | None = None

        # HTTP
        self._async_http_client: httpx.AsyncClient | None = None
        self._http_client: HttpClient | None = None

        # LLM
        self._groq_client: AsyncGroq | None = None
        self._groq_provider: GroqProvider | None = None
        self._llm_service: LLMService | None = None

        # Prompting
        self._prompt_builder: PromptBuilder | None = None
        self._context_formatter: SearchContextFormatter | None = None

        # Search
        self._tavily_provider: TavilyProvider | None = None
        self._search_service: SearchService | None = None
        self._search_ranker: SearchRanker | None = None
        self._search_ranking_service: SearchRankingService | None = None

        # Research
        self._router: LLMResearchRouter | None = None
        self._research_workflow: SimpleResearchWorkflow | None = None
        # Memory
        self._memory_repository: InMemoryMemoryRepository | None = None
        self._memory_service: MemoryService | None = None
        # Application services
        self._chat_service: ChatService | None = None

        # Summary
        
        self._summary_repository: InMemorySummaryRepository | None = None
        self._summary_service: SummaryService | None = None
        self._conversation_summarizer: ConversationSummarizer | None = None
        #Cache
        
        self._cache_repository: InMemoryResearchCacheRepository | None = None
        self._cache_matcher: ResearchCacheMatcher | None = None
        self._cache_service: ResearchCacheService | None = None

        self._prompt_cache_repository: InMemoryPromptCacheRepository | None = None
        self._prompt_cache_service: PromptCacheService | None = None
        self._prefix_builder: PrefixBuilder | None = None
        self._suffix_builder: SuffixBuilder | None = None        
    # -------------------------
    # Configuration
    # -------------------------

    @property
    def settings(self) -> Settings:

        if self._settings is None:
            self._settings = get_settings()

        return self._settings

    # -------------------------
    # HTTP
    # -------------------------

    @property
    def async_http_client(self) -> httpx.AsyncClient:

        if self._async_http_client is None:
            self._async_http_client = httpx.AsyncClient(
                timeout=30,
            )

        return self._async_http_client

    @property
    def http_client(self) -> HttpClient:

        if self._http_client is None:
            self._http_client = HttpClient(
                client=self.async_http_client,
            )

        return self._http_client

    # -------------------------
    # LLM
    # -------------------------

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

    # -------------------------
    # Prompting
    # -------------------------

    @property
    def prompt_builder(self) -> PromptBuilder:

        if self._prompt_builder is None:
            self._prompt_builder = PromptBuilder(
                prefix_builder=self.prefix_builder,
                suffix_builder=self.suffix_builder,
                prompt_cache=self.prompt_cache_service,
            )

        return self._prompt_builder

    # -------------------------
    # Search
    # -------------------------

    @property
    def tavily_provider(self) -> TavilyProvider:

        if self._tavily_provider is None:

            self._tavily_provider = TavilyProvider(
                client=AsyncTavilyClient(
                    api_key=self.settings.tavily_api_key,
                ),
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
    def search_ranker(self) -> SearchRanker:

        if self._search_ranker is None:
            self._search_ranker = JinaSearchRanker(
                client=self.http_client,
                api_key=self.settings.jina_api_key,
                base_url=self.settings.jina_base_url,
                model=self.settings.jina_reranker_model,
            )

        return self._search_ranker

    @property
    def search_ranking_service(self) -> SearchRankingService:

        if self._search_ranking_service is None:
            self._search_ranking_service = SearchRankingService(
                ranker=self.search_ranker,
            )

        return self._search_ranking_service

    # -------------------------
    # Research
    # -------------------------

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

    @property
    def research_workflow(self) -> SimpleResearchWorkflow:

        if self._research_workflow is None:
            self._research_workflow = SimpleResearchWorkflow(
                llm_service=self.llm_service,
                prompt_builder=self.prompt_builder,
                search_service=self.search_service,
                search_ranking_service=self.search_ranking_service,
                router=self.router,
                context_formatter=self.context_formatter,
                cache_service=self.cache_service,
            )

        return self._research_workflow

    # -------------------------
    # Application Services
    # -------------------------

    @property
    def chat_service(self) -> ChatService:

        if self._chat_service is None:
            self._chat_service = ChatService(
                workflow=self.research_workflow,
                memory_service=self.memory_service,
                 summary_service=self.summary_service,
                summarizer=self.conversation_summarizer,
            )

        return self._chat_service
    async def close(self) -> None:
        """
        Release managed resources.
        """

        if self._async_http_client is not None:
            await self._async_http_client.aclose()
    @property
    def context_formatter(self) -> SearchContextFormatter:

        if self._context_formatter is None:
            self._context_formatter = SearchContextFormatter()

        return self._context_formatter

    @property
    def memory_repository(self) -> InMemoryMemoryRepository:

        if self._memory_repository is None:
            self._memory_repository = InMemoryMemoryRepository()

        return self._memory_repository


    @property
    def memory_service(self) -> MemoryService:

        if self._memory_service is None:
            self._memory_service = MemoryService(
                repository=self.memory_repository,
            )

        return self._memory_service

    @property
    def summary_repository(self) -> InMemorySummaryRepository:

        if self._summary_repository is None:
            self._summary_repository = InMemorySummaryRepository()

        return self._summary_repository

    @property
    def summary_service(self) -> SummaryService:

        if self._summary_service is None:
            self._summary_service = SummaryService(
                repository=self.summary_repository,
            )

        return self._summary_service

    @property
    def conversation_summarizer(self) -> ConversationSummarizer:

        if self._conversation_summarizer is None:
            self._conversation_summarizer = ConversationSummarizer(
                llm_service=self.llm_service,
            )

        return self._conversation_summarizer

    @property
    def cache_repository(
        self,
    ) -> InMemoryResearchCacheRepository:

        if self._cache_repository is None:
            self._cache_repository = InMemoryResearchCacheRepository()

        return self._cache_repository

    @property
    def cache_matcher(
        self,
    ) -> ResearchCacheMatcher:

        if self._cache_matcher is None:
            self._cache_matcher = ResearchCacheMatcher()

        return self._cache_matcher

    
    @property
    def cache_service(
        self,
    ) -> ResearchCacheService:

        if self._cache_service is None:
            self._cache_service = ResearchCacheService(
                repository=self.cache_repository,
                matcher=self.cache_matcher,
            )

        return self._cache_service
    @property
    def prompt_cache_repository(self) -> InMemoryPromptCacheRepository:

        if self._prompt_cache_repository is None:
            self._prompt_cache_repository = InMemoryPromptCacheRepository()

        return self._prompt_cache_repository

    @property
    def prompt_cache_service(self) -> PromptCacheService:

        if self._prompt_cache_service is None:
            self._prompt_cache_service = PromptCacheService(
                repository=self.prompt_cache_repository,
            )

        return self._prompt_cache_service

    @property
    def prefix_builder(self) -> PrefixBuilder:
        if self._prefix_builder is None:
            self._prefix_builder = PrefixBuilder(
                Path("backend/app/ai/prompts/system.md")
            )
        return self._prefix_builder


    @property
    def suffix_builder(self) -> SuffixBuilder:
        if self._suffix_builder is None:
            self._suffix_builder = SuffixBuilder()
        return self._suffix_builder