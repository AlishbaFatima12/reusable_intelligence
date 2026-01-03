"""
Dapr client helpers for state management and pub/sub.

Provides simple interfaces for:
- Saving/retrieving state from Dapr state store (PostgreSQL)
- Publishing/subscribing via Dapr pub/sub
"""

import logging
import json
from typing import Any, Optional, Dict
from dapr.clients import DaprClient

logger = logging.getLogger(__name__)

DAPR_STATE_STORE_NAME = "statestore"
DAPR_PUBSUB_NAME = "kafka-pubsub"


class DaprStateClient:
    """Dapr state store client"""

    def __init__(self):
        self.client = DaprClient()

    def save_state(self, key: str, value: Any, ttl_seconds: Optional[int] = None):
        """Save state to Dapr state store"""
        try:
            metadata = {}
            if ttl_seconds:
                metadata["ttlInSeconds"] = str(ttl_seconds)

            self.client.save_state(
                store_name=DAPR_STATE_STORE_NAME,
                key=key,
                value=json.dumps(value) if not isinstance(value, str) else value,
                state_metadata=metadata
            )
            logger.info(f"Saved state for key: {key}")
        except Exception as e:
            logger.error(f"Failed to save state for {key}: {e}")
            raise

    def get_state(self, key: str) -> Optional[Any]:
        """Get state from Dapr state store"""
        try:
            response = self.client.get_state(
                store_name=DAPR_STATE_STORE_NAME,
                key=key
            )
            if response.data:
                return json.loads(response.data)
            return None
        except Exception as e:
            logger.error(f"Failed to get state for {key}: {e}")
            return None

    def delete_state(self, key: str):
        """Delete state from Dapr state store"""
        try:
            self.client.delete_state(
                store_name=DAPR_STATE_STORE_NAME,
                key=key
            )
            logger.info(f"Deleted state for key: {key}")
        except Exception as e:
            logger.error(f"Failed to delete state for {key}: {e}")
            raise


class DaprPubSubClient:
    """Dapr pub/sub client"""

    def __init__(self):
        self.client = DaprClient()

    def publish(self, topic: str, data: Dict[str, Any]):
        """Publish message via Dapr pub/sub"""
        try:
            self.client.publish_event(
                pubsub_name=DAPR_PUBSUB_NAME,
                topic_name=topic,
                data=json.dumps(data),
                data_content_type='application/json'
            )
            logger.info(f"Published event to topic: {topic}")
        except Exception as e:
            logger.error(f"Failed to publish to {topic}: {e}")
            raise
