"""
Kafka client wrappers for pub/sub messaging.

Provides simple interfaces for:
- Publishing messages to Kafka topics
- Subscribing to Kafka topics with consumer groups
- Handling message serialization/deserialization
"""

import json
import logging
from typing import Callable, Dict, Any, Optional
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
from .models import KafkaMessageEnvelope

logger = logging.getLogger(__name__)


class KafkaPublisher:
    """Kafka message publisher"""

    def __init__(self, bootstrap_servers: str = "localhost:9092"):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            compression_type='lz4',
            max_request_size=1048576,  # 1 MB
        )

    def publish(self, topic: str, message: KafkaMessageEnvelope, key: Optional[str] = None):
        """Publish message to Kafka topic"""
        try:
            message_dict = message.model_dump(mode='json')
            future = self.producer.send(
                topic,
                value=message_dict,
                key=key.encode('utf-8') if key else None
            )
            future.get(timeout=10)
            logger.info(f"Published message to {topic}: {message.event_type}")
        except KafkaError as e:
            logger.error(f"Failed to publish to {topic}: {e}")
            raise

    def close(self):
        """Close producer"""
        self.producer.close()


class KafkaSubscriber:
    """Kafka message subscriber"""

    def __init__(
        self,
        topic: str,
        group_id: str,
        bootstrap_servers: str = "localhost:9092"
    ):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='latest',
            enable_auto_commit=True,
        )

    def subscribe(self, handler: Callable[[Dict[str, Any]], None]):
        """Subscribe and handle messages"""
        logger.info(f"Starting to consume messages...")
        for message in self.consumer:
            try:
                handler(message.value)
            except Exception as e:
                logger.error(f"Error handling message: {e}")

    def close(self):
        """Close consumer"""
        self.consumer.close()
