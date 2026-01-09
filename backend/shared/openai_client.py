"""
OpenAI API wrapper with rate limiting and error handling.

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
from openai import OpenAI
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env files
load_dotenv()

logger = logging.getLogger(__name__)


class OpenAIClient:
    """OpenAI API client with rate limiting"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4o-mini",
        max_tokens: int = 4096,
        rate_limit: int = 60,  # requests per minute
        timeout: int = 30,
    ):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
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

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate response from OpenAI (async version for compatibility)"""
        result = self.generate_response(prompt=prompt, system_prompt=system_prompt)
        return result.get("response_text", "")

    def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_retries: int = 3,
    ) -> Dict[str, any]:
        """Generate response from OpenAI with retries"""
        for attempt in range(max_retries):
            try:
                self._wait_for_rate_limit()

                start_time = time.time()

                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})

                response = self.client.chat.completions.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    messages=messages,
                    timeout=self.timeout,
                )

                processing_time_ms = int((time.time() - start_time) * 1000)

                return {
                    "response_text": response.choices[0].message.content,
                    "model": self.model,
                    "token_count": response.usage.total_tokens,
                    "processing_time_ms": processing_time_ms,
                }

            except Exception as e:
                logger.error(f"OpenAI API error (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    sleep_time = 2 ** attempt  # Exponential backoff
                    time.sleep(sleep_time)
                else:
                    raise

        raise Exception("Failed to generate response after all retries")
