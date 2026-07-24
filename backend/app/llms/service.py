from backend.app.llms.interfaces import LLMProvider
from backend.app.llms.models import LLMRequest, LLMResponse


class LLMService:
    """
    Facade over the configured provider.

    Future responsibilities:

    - Prompt caching
    - Retries
    - Rate limiting
    - Metrics
    - Observability
    """

    def __init__(
        self,
        provider: LLMProvider,
    ) -> None:
        self._provider = provider

    async def invoke(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        return await self._provider.invoke(request)