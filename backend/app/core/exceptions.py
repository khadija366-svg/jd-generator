class LLMTimeoutError(Exception):
    """Raised when the OpenAI request times out."""


class LLMRateLimitError(Exception):
    """Raised when OpenAI returns a rate limit error."""


class LLMProviderError(Exception):
    """Raised for connection errors or non-2xx OpenAI responses."""


class LLMBadResponseError(Exception):
    """Raised when OpenAI returns an empty or unusable response."""
