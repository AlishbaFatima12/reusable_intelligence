"""
Concepts Agent API Routes

Endpoints for generating concept explanations.
"""

import logging
import time
from fastapi import APIRouter, HTTPException
from backend.agents.concepts.models import ConceptExplanationRequest, ConceptExplanationResponse
from backend.agents.concepts.services.explainer import ConceptExplainer
from backend.agents.concepts.services.state_manager import ConceptStateManager
from backend.shared.claude_client import ClaudeClient
from backend.shared.kafka_client import KafkaPublisher
from backend.shared.models import KafkaMessageEnvelope
from backend.shared.metrics import MetricsCollector, track_latency
from backend.agents.concepts.config import config

logger = logging.getLogger(__name__)

# Initialize dependencies
claude_client = ClaudeClient(
    model=config.claude_model,
    max_tokens=config.claude_max_tokens,
    rate_limit=config.claude_rate_limit,
    timeout=config.claude_timeout
)

explainer = ConceptExplainer(claude_client=claude_client)
state_manager = ConceptStateManager()
kafka_publisher = KafkaPublisher(bootstrap_servers=config.kafka_bootstrap_servers)
metrics = MetricsCollector(agent_name="concepts-agent")

router = APIRouter()


@router.post("/explain", response_model=ConceptExplanationResponse)
@track_latency(agent_name="concepts-agent", endpoint="explain")
async def explain_concept(request: ConceptExplanationRequest):
    """
    Generate explanation for a programming concept

    Flow:
    1. Check cache for existing explanation
    2. If not cached, generate using Claude API
    3. Cache the explanation
    4. Publish response to Kafka
    5. Return explanation
    """
    try:
        start_time = time.time()

        logger.info(
            f"Explaining concept: query_id={request.query_id}, "
            f"concept={request.concept}, level={request.difficulty_level}"
        )

        # Check cache first
        cached_explanation = None
        if config.enable_caching:
            cached_explanation = state_manager.get_cached_explanation(
                concept=request.concept,
                difficulty_level=request.difficulty_level
            )

        if cached_explanation:
            # Use cached explanation
            logger.info(f"Using cached explanation for: {request.concept}")
            metrics.track_request(endpoint="/explain", status="cache_hit")

            return cached_explanation

        # Generate new explanation
        explanation_data = await explainer.explain_concept(
            concept=request.concept,
            difficulty_level=request.difficulty_level,
            include_examples=request.include_examples,
            include_visualization=request.include_visualization
        )

        # Track Claude API metrics
        metrics.track_claude_call(
            model=config.claude_model,
            status="success",
            duration_seconds=explanation_data.get("processing_time_ms", 0) / 1000,
            input_tokens=explanation_data.get("token_count", 0) // 2,
            output_tokens=explanation_data.get("token_count", 0) // 2
        )

        processing_time = int((time.time() - start_time) * 1000)

        # Create response
        response = ConceptExplanationResponse(
            query_id=request.query_id,
            student_id=request.student_id,
            concept=request.concept,
            explanation=explanation_data["explanation"],
            code_examples=explanation_data.get("code_examples", []),
            visualization=explanation_data.get("visualization"),
            key_points=explanation_data.get("key_points", []),
            common_mistakes=explanation_data.get("common_mistakes", []),
            next_steps=explanation_data.get("next_steps"),
            processing_time_ms=processing_time
        )

        # Cache the explanation
        if config.enable_caching:
            state_manager.cache_explanation(
                concept=request.concept,
                difficulty_level=request.difficulty_level,
                explanation=response
            )

        # Publish response to Kafka
        envelope = KafkaMessageEnvelope(
            event_type="concept_explained",
            service_name="concepts-agent",
            data={
                "query_id": request.query_id,
                "student_id": request.student_id,
                "concept": request.concept,
                "response": response.model_dump()
            }
        )

        kafka_publisher.publish(
            topic="agent-responses",
            message=envelope,
            key=request.student_id
        )

        metrics.track_kafka_message(topic="agent-responses", status="success")
        metrics.track_request(endpoint="/explain", status="success")

        logger.info(
            f"Explanation generated: query_id={request.query_id}, "
            f"processing_time={processing_time}ms"
        )

        return response

    except Exception as e:
        logger.error(f"Error explaining concept {request.concept}: {e}", exc_info=True)
        metrics.track_request(endpoint="/explain", status="error")
        raise HTTPException(status_code=500, detail=f"Explanation generation failed: {str(e)}")


@router.get("/concepts/popular")
async def get_popular_concepts():
    """
    Get list of popular concepts (placeholder for future implementation)

    Could track most requested concepts from cache hit counts.
    """
    return {
        "popular_concepts": [
            "variables and data types",
            "functions",
            "loops",
            "lists and dictionaries",
            "object-oriented programming",
            "recursion",
            "file I/O",
            "error handling"
        ]
    }


@router.get("/stats")
async def get_stats():
    """
    Get Concepts Agent statistics

    Returns basic stats about processed queries.
    """
    return {
        "agent": "concepts-agent",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": ["/explain", "/concepts/popular", "/health", "/ready", "/stats"]
    }
