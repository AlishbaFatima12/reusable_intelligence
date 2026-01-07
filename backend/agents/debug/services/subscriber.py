"""
Kafka Subscriber for Debug Agent

Subscribes to debug-queries topic and processes error diagnosis requests.
"""

import logging
import asyncio
from typing import Callable
from backend.shared.kafka_client import KafkaSubscriber
from backend.shared.models import KafkaMessageEnvelope

logger = logging.getLogger(__name__)


class DebugSubscriber:
    """
    Subscribes to debug-queries Kafka topic and processes diagnosis requests
    """

    def __init__(
        self,
        kafka_bootstrap_servers: str,
        group_id: str = "debug-agent-consumer"
    ):
        """
        Initialize DebugSubscriber

        Args:
            kafka_bootstrap_servers: Kafka bootstrap servers
            group_id: Kafka consumer group ID
        """
        self.subscriber = KafkaSubscriber(
            bootstrap_servers=kafka_bootstrap_servers,
            group_id=group_id,
            topics=["debug-queries"]
        )

    async def start(self, message_handler: Callable):
        """
        Start consuming messages from Kafka

        Args:
            message_handler: Async function to handle each message
                            Should accept (message: KafkaMessageEnvelope)
        """
        logger.info("Starting Debug Agent Kafka subscriber...")

        try:
            await self.subscriber.consume(callback=message_handler)
        except Exception as e:
            logger.error(f"Error in Debug subscriber: {e}", exc_info=True)
            raise

    def stop(self):
        """Stop consuming messages"""
        logger.info("Stopping Debug Agent Kafka subscriber...")
        self.subscriber.close()
