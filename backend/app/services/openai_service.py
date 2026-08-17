from openai import OpenAI, APITimeoutError, APIConnectionError, RateLimitError, APIStatusError

from app.core.config import settings
from app.core.exceptions import (
    LLMTimeoutError,
    LLMRateLimitError,
    LLMProviderError,
    LLMBadResponseError,
)

_client = OpenAI(api_key=settings.OPENAI_API_KEY, base_url="https://api.groq.com/openai/v1")

def generate_completion(system_prompt: str, user_content: str) -> str:
    """
    Send a single system+user message pair to GPT-5.6 and return the plain text reply.
    This is the only function in the codebase that talks to OpenAI.
    """
    try:
        response = _client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            timeout=settings.REQUEST_TIMEOUT_SECONDS,
        )
    except APITimeoutError:
        raise LLMTimeoutError("The request to the AI provider timed out.")
    except RateLimitError:
        raise LLMRateLimitError("The AI provider rate limit was hit.")
    except APIConnectionError:
        raise LLMProviderError("Could not connect to the AI provider.")
    except APIStatusError as e:
        print(f"DEBUG OpenAI error: {e.status_code} - {e.message}")
        raise LLMProviderError(f"The AI provider returned an error (status {e.status_code}).")

    if not response.choices or not response.choices[0].message.content:
        raise LLMBadResponseError("The AI provider returned an empty response.")

    return response.choices[0].message.content.strip()
