"""
Dapr client helpers for state management and pub/sub.

Provides simple interfaces for:
- Saving/retrieving state from Dapr state store (PostgreSQL)
- Publishing/subscribing via Dapr pub/sub

Falls back to in-memory storage when Dapr is not available (dev mode).
"""

import logging
import json
import os
from typing import Any, Optional, Dict

logger = logging.getLogger(__name__)

DAPR_STATE_STORE_NAME = "statestore"
DAPR_PUBSUB_NAME = "kafka-pubsub"

# Try to import Dapr, fall back to mock if not available
DAPR_AVAILABLE = False
try:
    from dapr.clients import DaprClient
    DAPR_AVAILABLE = True
    logger.info("Dapr SDK available - will use Dapr when daemon is running")
except ImportError:
    logger.warning("Dapr SDK not installed - using in-memory fallback (dev mode)")

# Check if running in development mode without Dapr
USE_DAPR = DAPR_AVAILABLE and os.getenv("USE_DAPR", "false").lower() == "true"


class DaprStateClient:
    """Dapr state store client with in-memory fallback for dev mode"""

    # In-memory storage for dev mode (shared across instances)
    _memory_store: Dict[str, Any] = {}

    def __init__(self):
        if USE_DAPR:
            self.client = DaprClient()
            logger.info("DaprStateClient initialized with Dapr daemon")
        else:
            self.client = None
            logger.info("DaprStateClient initialized with in-memory storage (dev mode)")

    def save_state(self, key: str, value: Any, ttl_seconds: Optional[int] = None):
        """Save state to Dapr state store or in-memory fallback"""
        try:
            if USE_DAPR and self.client:
                metadata = {}
                if ttl_seconds:
                    metadata["ttlInSeconds"] = str(ttl_seconds)

                self.client.save_state(
                    store_name=DAPR_STATE_STORE_NAME,
                    key=key,
                    value=json.dumps(value) if not isinstance(value, str) else value,
                    state_metadata=metadata
                )
                logger.info(f"[Dapr] Saved state for key: {key}")
            else:
                # In-memory fallback
                self._memory_store[key] = value
                logger.debug(f"[Memory] Saved state for key: {key}")
        except Exception as e:
            logger.error(f"Failed to save state for {key}: {e}")
            raise

    def get_state(self, key: str) -> Optional[Any]:
        """Get state from Dapr state store or in-memory fallback"""
        try:
            if USE_DAPR and self.client:
                response = self.client.get_state(
                    store_name=DAPR_STATE_STORE_NAME,
                    key=key
                )
                if response.data:
                    return json.loads(response.data)
                return None
            else:
                # In-memory fallback
                return self._memory_store.get(key)
        except Exception as e:
            logger.error(f"Failed to get state for {key}: {e}")
            return None

    def delete_state(self, key: str):
        """Delete state from Dapr state store or in-memory fallback"""
        try:
            if USE_DAPR and self.client:
                self.client.delete_state(
                    store_name=DAPR_STATE_STORE_NAME,
                    key=key
                )
                logger.info(f"[Dapr] Deleted state for key: {key}")
            else:
                # In-memory fallback
                self._memory_store.pop(key, None)
                logger.debug(f"[Memory] Deleted state for key: {key}")
        except Exception as e:
            logger.error(f"Failed to delete state for {key}: {e}")
            raise


class DaprPubSubClient:
    """Dapr pub/sub client with logging fallback for dev mode"""

    def __init__(self):
        if USE_DAPR:
            self.client = DaprClient()
            logger.info("DaprPubSubClient initialized with Dapr daemon")
        else:
            self.client = None
            logger.info("DaprPubSubClient initialized with logging fallback (dev mode)")

    def publish(self, topic: str, data: Dict[str, Any]):
        """Publish message via Dapr pub/sub or log in dev mode"""
        try:
            if USE_DAPR and self.client:
                self.client.publish_event(
                    pubsub_name=DAPR_PUBSUB_NAME,
                    topic_name=topic,
                    data=json.dumps(data),
                    data_content_type='application/json'
                )
                logger.info(f"[Dapr] Published event to topic: {topic}")
            else:
                # Logging fallback - just log the event
                logger.info(f"[Memory] Would publish to topic '{topic}': {json.dumps(data, indent=2)}")
        except Exception as e:
            logger.error(f"Failed to publish to {topic}: {e}")
            raise
