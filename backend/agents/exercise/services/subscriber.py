"""
Kafka Subscriber for Exercise Generator

Subscribes to exercise-queries topic and processes exercise generation requests.
"""

import logging
import asyncio
from typing import Callable
from backend.shared.kafka_client import KafkaSubscriber
from backend.shared.models import KafkaMessageEnvelope

logger = logging.getLogger(__name__)


class ExerciseSubscriber:
    """
    Subscribes to exercise-queries Kafka topic and processes generation requests
    """

    def __init__(
        self,
        kafka_bootstrap_servers: str,
        group_id: str = "exercise-generator-consumer"
    ):
        """
        Initialize ExerciseSubscriber

        Args:
            kafka_bootstrap_servers: Kafka bootstrap servers
            group_id: Kafka consumer group ID
        """
        self.subscriber = KafkaSubscriber(
            bootstrap_servers=kafka_bootstrap_servers,
            group_id=group_id,
            topics=["exercise-queries"]
        )

    async def start(self, message_handler: Callable):
        """
        Start consuming messages from Kafka

        Args:
            message_handler: Async function to handle each message
                            Should accept (message: KafkaMessageEnvelope)
        """
        logger.info("Starting Exercise Generator Kafka subscriber...")

        try:
            await self.subscriber.consume(callback=message_handler)
        except Exception as e:
            logger.error(f"Error in Exercise subscriber: {e}", exc_info=True)
            raise

    def stop(self):
        """Stop consuming messages"""
        logger.info("Stopping Exercise Generator Kafka subscriber...")
        self.subscriber.close()
