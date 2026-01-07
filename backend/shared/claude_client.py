"""
Anthropic Claude API wrapper with rate limiting and error handling.

Provides:
- Rate limiting (60 requests/minute default)
- Automatic retries with exponential backoff
- Timeout handling
- Token counting
- Error handling
"""

import os
import time
import logging
from typing import Optional, List, Dict
from anthropic import Anthropic, APIError, RateLimitError
import asyncio

logger = logging.getLogger(__name__)


class ClaudeClient:
    """Claude API client with rate limiting"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-sonnet-3-5-20241022",
        max_tokens: int = 4096,
        rate_limit: int = 60,  # requests per minute
        timeout: int = 30,
    ):
        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
        self.model = model
        self.max_tokens = max_tokens
        self.rate_limit = rate_limit
        self.timeout = timeout
        self.last_request_time = 0
        self.request_count = 0

    def _wait_for_rate_limit(self):
        """Implement rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time

        # Reset counter every minute
        if time_since_last > 60:
            self.request_count = 0
            self.last_request_time = current_time

        # Check if we've hit rate limit
        if self.request_count >= self.rate_limit:
            sleep_time = 60 - time_since_last
            if sleep_time > 0:
                logger.warning(f"Rate limit reached, sleeping for {sleep_time:.2f}s")
                time.sleep(sleep_time)
                self.request_count = 0
                self.last_request_time = time.time()

        self.request_count += 1

    def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_retries: int = 3,
    ) -> Dict[str, any]:
        """Generate response from Claude with retries"""
        for attempt in range(max_retries):
            try:
                self._wait_for_rate_limit()

                start_time = time.time()

                messages = [{"role": "user", "content": prompt}]

                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    system=system_prompt or "",
                    messages=messages,
                    timeout=self.timeout,
                )

                processing_time_ms = int((time.time() - start_time) * 1000)

                return {
                    "response_text": response.content[0].text,
                    "model": self.model,
                    "token_count": response.usage.input_tokens + response.usage.output_tokens,
                    "processing_time_ms": processing_time_ms,
                }

            except RateLimitError as e:
                logger.warning(f"Rate limit error (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    sleep_time = 2 ** attempt  # Exponential backoff
                    time.sleep(sleep_time)
                else:
                    raise

            except APIError as e:
                logger.error(f"Claude API error (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                else:
                    raise

            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                raise

        raise Exception("Failed to generate response after all retries")

    def generate_streaming_response(self, prompt: str, system_prompt: Optional[str] = None):
        """Generate streaming response (for future use)"""
        self._wait_for_rate_limit()

        messages = [{"role": "user", "content": prompt}]

        with self.client.messages.stream(
            model=self.model,
            max_tokens=self.max_tokens,
            system=system_prompt or "",
            messages=messages,
        ) as stream:
            for text in stream.text_stream:
                yield text
