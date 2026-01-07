"""
Kafka client wrappers for pub/sub messaging.

Provides simple interfaces for:
- Publishing messages to Kafka topics
- Subscribing to Kafka topics with consumer groups
- Handling message serialization/deserialization

Falls back to logging when Kafka is not available (dev mode).
"""

import json
import logging
import os
from typing import Callable, Dict, Any, Optional
from .models import KafkaMessageEnvelope

logger = logging.getLogger(__name__)

# Try to import Kafka, fall back to mock if not available
KAFKA_AVAILABLE = False
KafkaError = Exception  # Fallback error class

try:
    from kafka import KafkaProducer, KafkaConsumer
    from kafka.errors import KafkaError
    KAFKA_AVAILABLE = True
    logger.info("Kafka SDK available - will use Kafka when broker is running")
except ImportError:
    logger.warning("Kafka SDK not installed - using logging fallback (dev mode)")

# Check if running in development mode without Kafka
USE_KAFKA = KAFKA_AVAILABLE and os.getenv("USE_KAFKA", "false").lower() == "true"


class KafkaPublisher:
    """Kafka message publisher with logging fallback for dev mode"""

    def __init__(self, bootstrap_servers: str = "localhost:9092"):
        if USE_KAFKA:
            self.producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                compression_type='lz4',
                max_request_size=1048576,  # 1 MB
            )
            logger.info("KafkaPublisher initialized with Kafka broker")
        else:
            self.producer = None
            logger.info("KafkaPublisher initialized with logging fallback (dev mode)")

    def publish(self, topic: str, message: KafkaMessageEnvelope, key: Optional[str] = None):
        """Publish message to Kafka topic or log in dev mode"""
        try:
            message_dict = message.model_dump(mode='json')

            if USE_KAFKA and self.producer:
                future = self.producer.send(
                    topic,
                    value=message_dict,
                    key=key.encode('utf-8') if key else None
                )
                future.get(timeout=10)
                logger.info(f"[Kafka] Published message to {topic}: {message.event_type}")
            else:
                # Logging fallback - just log the event
                logger.info(f"[Memory] Would publish to topic '{topic}' (event: {message.event_type})")
                logger.debug(f"[Memory] Message data: {json.dumps(message_dict, indent=2)}")
        except KafkaError as e:
            logger.error(f"Failed to publish to {topic}: {e}")
            raise

    def close(self):
        """Close producer"""
        if self.producer:
            self.producer.close()


class KafkaSubscriber:
    """Kafka message subscriber with no-op fallback for dev mode"""

    def __init__(
        self,
        topic: str,
        group_id: str,
        bootstrap_servers: str = "localhost:9092"
    ):
        self.topic = topic
        self.group_id = group_id

        if USE_KAFKA:
            self.consumer = KafkaConsumer(
                topic,
                bootstrap_servers=bootstrap_servers,
                group_id=group_id,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='latest',
                enable_auto_commit=True,
            )
            logger.info(f"KafkaSubscriber initialized with Kafka broker for topic: {topic}")
        else:
            self.consumer = None
            logger.info(f"KafkaSubscriber initialized with no-op fallback (dev mode) for topic: {topic}")

    def subscribe(self, handler: Callable[[Dict[str, Any]], None]):
        """Subscribe and handle messages or no-op in dev mode"""
        if USE_KAFKA and self.consumer:
            logger.info(f"Starting to consume messages from {self.topic}...")
            for message in self.consumer:
                try:
                    handler(message.value)
                except Exception as e:
                    logger.error(f"Error handling message: {e}")
        else:
            logger.info(f"[Memory] Subscriber for '{self.topic}' is in no-op mode (dev mode)")
            # In dev mode, subscriber doesn't do anything since there's no Kafka

    def close(self):
        """Close consumer"""
        if self.consumer:
            self.consumer.close()
