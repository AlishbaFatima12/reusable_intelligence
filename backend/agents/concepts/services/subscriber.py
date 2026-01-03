"""
Kafka Subscriber for Concepts Queries

Subscribes to concepts-queries topic and processes incoming concept explanation requests.
"""

import logging
import json
from typing import Callable, Dict, Any
from backend.shared.kafka_client import KafkaSubscriber
from backend.shared.models import KafkaMessageEnvelope, StudentQuery

logger = logging.getLogger(__name__)


class ConceptsSubscriber:
    """Subscribes to concept query Kafka topic"""

    def __init__(
        self,
        bootstrap_servers: str,
        group_id: str = "concepts-agent-group"
    ):
        self.subscriber = KafkaSubscriber(
            topic="concepts-queries",
            group_id=group_id,
            bootstrap_servers=bootstrap_servers
        )

    def start_consuming(self, message_handler: Callable[[Dict[str, Any]], None]):
        """
        Start consuming messages from concepts-queries topic

        Args:
            message_handler: Function to handle each incoming message
        """
        logger.info("Starting to consume from concepts-queries topic...")

        def handle_message(message_data: Dict[str, Any]):
            """Process incoming Kafka message"""
            try:
                # Extract student query from message envelope
                if "data" in message_data and "original_query" in message_data["data"]:
                    query_data = message_data["data"]["original_query"]
                    student_query = StudentQuery(**query_data)

                    logger.info(
                        f"Received concept query: query_id={student_query.query_id}, "
                        f"student_id={student_query.student_id}"
                    )

                    # Call the message handler
                    message_handler(student_query.model_dump())

                else:
                    logger.warning(f"Invalid message format: {message_data}")

            except Exception as e:
                logger.error(f"Error processing message: {e}", exc_info=True)

        # Start consuming
        self.subscriber.subscribe(handler=handle_message)

    def close(self):
        """Close Kafka subscriber"""
        self.subscriber.close()
