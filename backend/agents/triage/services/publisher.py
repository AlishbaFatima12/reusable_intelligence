"""
Kafka Publisher for Routing Decisions

Publishes routing decisions to appropriate Kafka topics.
"""

import logging
from typing import Dict, Any
from backend.shared.kafka_client import KafkaPublisher
from backend.shared.models import KafkaMessageEnvelope, IntentType
from backend.agents.triage.models import RoutingDecision

logger = logging.getLogger(__name__)


class RoutingPublisher:
    """Publishes routing decisions to Kafka"""

    # Topic mapping based on intent
    TOPIC_MAP = {
        IntentType.CONCEPT: "concepts-queries",
        IntentType.CODE_REVIEW: "code-review-queries",
        IntentType.DEBUG: "debug-queries",
        IntentType.EXERCISE: "exercise-queries",
        IntentType.PROGRESS: "progress-queries",
        IntentType.UNCLEAR: "concepts-queries",  # Default to concepts for unclear intent
    }

    def __init__(self, kafka_bootstrap_servers: str):
        self.publisher = KafkaPublisher(bootstrap_servers=kafka_bootstrap_servers)

    def publish_routing_decision(
        self,
        routing_decision: RoutingDecision
    ) -> None:
        """
        Publish routing decision to appropriate Kafka topic

        Args:
            routing_decision: The routing decision to publish
        """
        # Determine target topic based on intent
        target_topic = self.TOPIC_MAP.get(
            routing_decision.detected_intent,
            "concepts-queries"  # Default fallback
        )

        # Also publish to triage-routing topic for monitoring
        self._publish_to_topic(
            topic="triage-routing",
            routing_decision=routing_decision,
            event_type="routing_decision"
        )

        # Publish to specialist agent topic
        self._publish_to_topic(
            topic=target_topic,
            routing_decision=routing_decision,
            event_type="query_routed"
        )

        logger.info(
            f"Published routing decision: query_id={routing_decision.query_id}, "
            f"intent={routing_decision.detected_intent.value}, "
            f"agent={routing_decision.routed_to_agent}, "
            f"topic={target_topic}"
        )

    def _publish_to_topic(
        self,
        topic: str,
        routing_decision: RoutingDecision,
        event_type: str
    ) -> None:
        """
        Publish message to specific Kafka topic

        Args:
            topic: Target Kafka topic
            routing_decision: Routing decision data
            event_type: Type of event
        """
        # Create Kafka message envelope
        envelope = KafkaMessageEnvelope(
            trace_id=routing_decision.query_id,
            event_type=event_type,
            payload={
                "query_id": routing_decision.query_id,
                "student_id": routing_decision.student_id,
                "detected_intent": routing_decision.detected_intent.value,
                "routed_to_agent": routing_decision.routed_to_agent,
                "confidence_score": routing_decision.confidence_score,
                "original_query": routing_decision.original_query.model_dump()
            },
            metadata={
                "service_name": "triage-agent"
            }
        )

        # Publish to Kafka (use student_id as key for partitioning)
        self.publisher.publish(
            topic=topic,
            message=envelope,
            key=routing_decision.student_id
        )

    def close(self):
        """Close Kafka publisher"""
        self.publisher.close()
