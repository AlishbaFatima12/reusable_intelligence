"""
Triage Agent API Routes

Endpoints for query analysis and routing.
"""

import logging
import time
from fastapi import APIRouter, HTTPException, Depends
from backend.agents.triage.models import QueryAnalysisRequest, QueryAnalysisResponse, RoutingDecision
from backend.agents.triage.services.classifier import IntentClassifier
from backend.agents.triage.services.publisher import RoutingPublisher
from backend.shared.claude_client import ClaudeClient
from backend.shared.models import StudentQuery, QueryStatus
from backend.shared.metrics import MetricsCollector, track_latency
from backend.agents.triage.config import config

logger = logging.getLogger(__name__)

# Initialize dependencies
claude_client = ClaudeClient(
    model=config.claude_model,
    max_tokens=config.claude_max_tokens,
    rate_limit=config.claude_rate_limit,
    timeout=config.claude_timeout
)

classifier = IntentClassifier(claude_client=claude_client)
publisher = RoutingPublisher(kafka_bootstrap_servers=config.kafka_bootstrap_servers)
metrics = MetricsCollector(agent_name="triage-agent")

router = APIRouter()


@router.post("/analyze", response_model=QueryAnalysisResponse)
@track_latency(agent_name="triage-agent", endpoint="analyze")
async def analyze_query(request: QueryAnalysisRequest):
    """
    Analyze student query and route to appropriate specialist agent

    Flow:
    1. Classify intent using Claude API
    2. Extract entities and determine confidence
    3. Publish routing decision to Kafka
    4. Return analysis result
    """
    try:
        start_time = time.time()

        # Log incoming request
        logger.info(f"Analyzing query: query_id={request.query_id}, student_id={request.student_id}")

        # Classify query intent
        classification = await classifier.classify_query(
            query_text=request.query_text,
            code_snippet=request.code_snippet,
            learning_context=request.learning_context
        )

        # Track Claude API metrics
        metrics.track_claude_call(
            model=config.claude_model,
            status="success" if classification else "error",
            duration_seconds=classification.get("processing_time_ms", 0) / 1000,
            input_tokens=classification.get("token_count", 0) // 2,  # Rough estimate
            output_tokens=classification.get("token_count", 0) // 2
        )

        # Check confidence threshold
        if classification["confidence"] < config.routing_confidence_threshold:
            logger.warning(
                f"Low confidence routing: query_id={request.query_id}, "
                f"confidence={classification['confidence']:.2f}"
            )

        # Create StudentQuery object
        student_query = StudentQuery(
            query_id=request.query_id,
            student_id=request.student_id,
            query_text=request.query_text,
            code_snippet=request.code_snippet,
            detected_intent=classification["intent"],
            routed_to_agent=classification["routed_to_agent"],
            status=QueryStatus.ROUTED
        )

        # Create routing decision
        routing_decision = RoutingDecision(
            query_id=request.query_id,
            student_id=request.student_id,
            detected_intent=classification["intent"],
            routed_to_agent=classification["routed_to_agent"],
            confidence_score=classification["confidence"],
            target_topic=publisher.TOPIC_MAP.get(classification["intent"], "concepts-queries"),
            original_query=student_query
        )

        # Publish to Kafka
        publisher.publish_routing_decision(routing_decision)

        # Track successful routing
        metrics.track_kafka_message(topic="triage-routing", status="success")
        metrics.track_request(endpoint="/analyze", status="success")

        processing_time = int((time.time() - start_time) * 1000)

        # Return response
        return QueryAnalysisResponse(
            query_id=request.query_id,
            detected_intent=classification["intent"],
            confidence_score=classification["confidence"],
            routed_to_agent=classification["routed_to_agent"],
            extracted_entities=classification.get("entities", {}),
            reasoning=classification.get("reasoning"),
            processing_time_ms=processing_time
        )

    except Exception as e:
        logger.error(f"Error analyzing query {request.query_id}: {e}", exc_info=True)
        metrics.track_request(endpoint="/analyze", status="error")
        raise HTTPException(status_code=500, detail=f"Query analysis failed: {str(e)}")


@router.get("/stats")
async def get_stats():
    """
    Get Triage Agent statistics

    Returns basic stats about processed queries.
    """
    return {
        "agent": "triage-agent",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": ["/analyze", "/health", "/ready", "/stats"]
    }
