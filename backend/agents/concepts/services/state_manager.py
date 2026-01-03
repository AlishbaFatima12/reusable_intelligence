"""
State Manager for Caching Concept Explanations

Uses Dapr state store to cache frequently requested concept explanations.
"""

import logging
import time
from typing import Optional
from backend.shared.dapr_client import DaprStateClient
from backend.agents.concepts.models import CachedExplanation, ConceptExplanationResponse

logger = logging.getLogger(__name__)


class ConceptStateManager:
    """Manages caching of concept explanations using Dapr state store"""

    # Cache TTL: 7 days (explanations don't change frequently)
    CACHE_TTL_SECONDS = 7 * 24 * 60 * 60

    def __init__(self):
        self.state_client = DaprStateClient()

    def get_cached_explanation(
        self,
        concept: str,
        difficulty_level: str = "beginner"
    ) -> Optional[ConceptExplanationResponse]:
        """
        Retrieve cached explanation from state store

        Args:
            concept: The concept name
            difficulty_level: Difficulty level

        Returns:
            Cached explanation if found, None otherwise
        """
        cache_key = self._get_cache_key(concept, difficulty_level)

        try:
            cached_data = self.state_client.get_state(cache_key)

            if cached_data:
                cached = CachedExplanation(**cached_data)

                # Update hit count
                cached.hit_count += 1
                self.state_client.save_state(
                    key=cache_key,
                    value=cached.model_dump(),
                    ttl_seconds=self.CACHE_TTL_SECONDS
                )

                logger.info(
                    f"Cache hit: concept={concept}, difficulty={difficulty_level}, "
                    f"hits={cached.hit_count}"
                )

                return cached.explanation

            logger.info(f"Cache miss: concept={concept}, difficulty={difficulty_level}")
            return None

        except Exception as e:
            logger.error(f"Error retrieving cached explanation: {e}")
            return None

    def cache_explanation(
        self,
        concept: str,
        difficulty_level: str,
        explanation: ConceptExplanationResponse
    ):
        """
        Cache explanation in state store

        Args:
            concept: The concept name
            difficulty_level: Difficulty level
            explanation: The explanation to cache
        """
        cache_key = self._get_cache_key(concept, difficulty_level)

        try:
            cached = CachedExplanation(
                concept=concept,
                difficulty_level=difficulty_level,
                explanation=explanation,
                cache_timestamp=int(time.time()),
                hit_count=0
            )

            self.state_client.save_state(
                key=cache_key,
                value=cached.model_dump(),
                ttl_seconds=self.CACHE_TTL_SECONDS
            )

            logger.info(f"Cached explanation: concept={concept}, difficulty={difficulty_level}")

        except Exception as e:
            logger.error(f"Error caching explanation: {e}")

    def invalidate_cache(self, concept: str, difficulty_level: str):
        """
        Invalidate cached explanation

        Args:
            concept: The concept name
            difficulty_level: Difficulty level
        """
        cache_key = self._get_cache_key(concept, difficulty_level)

        try:
            self.state_client.delete_state(cache_key)
            logger.info(f"Invalidated cache: concept={concept}, difficulty={difficulty_level}")
        except Exception as e:
            logger.error(f"Error invalidating cache: {e}")

    def _get_cache_key(self, concept: str, difficulty_level: str) -> str:
        """
        Generate cache key for concept explanation

        Args:
            concept: The concept name
            difficulty_level: Difficulty level

        Returns:
            Cache key string
        """
        # Normalize concept name (lowercase, remove spaces)
        normalized_concept = concept.lower().replace(" ", "_")
        return f"concept_explanation:{normalized_concept}:{difficulty_level}"
