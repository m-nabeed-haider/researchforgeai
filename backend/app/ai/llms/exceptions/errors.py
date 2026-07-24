class LLMProviderError(Exception):
    """Base exception for all LLM provider errors."""


class AuthenticationError(LLMProviderError):
    """Raised when provider authentication fails."""


class RateLimitError(LLMProviderError):
    """Raised when provider rate limits are exceeded."""


class ModelNotFoundError(LLMProviderError):
    """Raised when the configured model does not exist."""
