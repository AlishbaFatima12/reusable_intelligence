"""
Kafka Subscriber for Code Review Requests

Subscribes to code-review-queries topic and processes incoming code review requests.
"""

import logging
import json
from typing import Callable, Dict, Any
from backend.shared.kafka_client import KafkaSubscriber
from backend.shared.models import KafkaMessageEnvelope, StudentQuery

logger = logging.getLogger(__name__)


class CodeReviewSubscriber:
    """Subscribes to code review request Kafka topic"""

    def __init__(
        self,
        bootstrap_servers: str,
        group_id: str = "code-review-agent-group"
    ):
        self.subscriber = KafkaSubscriber(
            topic="code-review-queries",
            group_id=group_id,
            bootstrap_servers=bootstrap_servers
        )

    def start_consuming(self, message_handler: Callable[[Dict[str, Any]], None]):
        """
        Start consuming messages from code-review-queries topic

        Args:
            message_handler: Function to handle each incoming message
        """
        logger.info("Starting to consume from code-review-queries topic...")

        def handle_message(message_data: Dict[str, Any]):
            """Process incoming Kafka message"""
            try:
                # Extract student query from message envelope
                if "data" in message_data and "original_query" in message_data["data"]:
                    query_data = message_data["data"]["original_query"]
                    student_query = StudentQuery(**query_data)

                    logger.info(
                        f"Received code review request: query_id={student_query.query_id}, "
                        f"student_id={student_query.student_id}"
                    )

                    # Pass to handler
                    message_handler(query_data)

                else:
                    logger.warning(f"Invalid message format: missing query data")

            except Exception as e:
                logger.error(f"Error processing code review message: {e}", exc_info=True)

        # Start consuming
        self.subscriber.consume_messages(handle_message)

    def stop(self):
        """Stop consuming messages"""
        logger.info("Stopping code review subscriber...")
        self.subscriber.close()
