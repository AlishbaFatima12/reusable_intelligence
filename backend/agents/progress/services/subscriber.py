"""
Kafka Subscriber for Agent Responses

Subscribes to agent-responses topic to track student progress.
"""

import logging
from typing import Callable, Dict, Any
from backend.shared.kafka_client import KafkaSubscriber

logger = logging.getLogger(__name__)


class ProgressSubscriber:
    """Subscribes to agent response Kafka topic"""

    def __init__(
        self,
        bootstrap_servers: str,
        group_id: str = "progress-tracker-group"
    ):
        self.subscriber = KafkaSubscriber(
            topic="agent-responses",
            group_id=group_id,
            bootstrap_servers=bootstrap_servers
        )

    def start_consuming(self, message_handler: Callable[[Dict[str, Any]], None]):
        """
        Start consuming messages from agent-responses topic

        Args:
            message_handler: Function to handle each incoming message
        """
        logger.info("Starting to consume from agent-responses topic...")

        def handle_message(message_data: Dict[str, Any]):
            """Process incoming Kafka message"""
            try:
                # Extract response data from message envelope
                if "data" in message_data:
                    response_data = message_data["data"]
                    student_id = response_data.get("student_id")
                    query_id = response_data.get("query_id")

                    if student_id:
                        logger.info(
                            f"Received agent response: query_id={query_id}, student_id={student_id}"
                        )

                        # Call the message handler
                        message_handler(response_data)
                    else:
                        logger.warning(f"Response missing student_id: {response_data}")
                else:
                    logger.warning(f"Invalid message format: {message_data}")

            except Exception as e:
                logger.error(f"Error processing message: {e}", exc_info=True)

        # Start consuming
        self.subscriber.subscribe(handler=handle_message)

    def close(self):
        """Close Kafka subscriber"""
        self.subscriber.close()
