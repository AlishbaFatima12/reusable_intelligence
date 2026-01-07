"""
Code Review Agent API Routes

Endpoints for code quality feedback and analysis.
"""

import logging
import time
from fastapi import APIRouter, HTTPException
from backend.agents.code_review.models import CodeReviewRequest, CodeReviewResponse
from backend.agents.code_review.services.reviewer import CodeReviewer
from backend.shared.claude_client import ClaudeClient
from backend.shared.kafka_client import KafkaPublisher
from backend.shared.models import KafkaMessageEnvelope
from backend.shared.metrics import MetricsCollector, track_latency
from backend.agents.code_review.config import config

logger = logging.getLogger(__name__)

# Initialize dependencies
claude_client = ClaudeClient(
    model=config.claude_model,
    max_tokens=config.claude_max_tokens,
    rate_limit=config.claude_rate_limit,
    timeout=config.claude_timeout
)

reviewer = CodeReviewer(claude_client=claude_client)
kafka_publisher = KafkaPublisher(bootstrap_servers=config.kafka_bootstrap_servers)
metrics = MetricsCollector(agent_name="code-review-agent")

router = APIRouter()


@router.post("/review", response_model=CodeReviewResponse)
@track_latency(agent_name="code-review-agent", endpoint="review")
async def review_code(request: CodeReviewRequest):
    """
    Review student code and provide quality feedback

    Flow:
    1. Analyze code using Claude API
    2. Extract feedback items, strengths, improvements
    3. Publish response to Kafka
    4. Return review result
    """
    try:
        start_time = time.time()

        logger.info(
            f"Reviewing code: query_id={request.query_id}, "
            f"language={request.language}, code_length={len(request.code)}"
        )

        # Validate code length
        if len(request.code) > config.max_code_length:
            raise HTTPException(
                status_code=400,
                detail=f"Code exceeds maximum length of {config.max_code_length} characters"
            )

        # Review code
        review_data = await reviewer.review_code(
            code=request.code,
            language=request.language,
            context=request.context,
            review_depth=config.review_depth
        )

        # Track Claude API metrics
        metrics.track_claude_call(
            model=config.claude_model,
            status="success",
            duration_seconds=review_data.get("processing_time_ms", 0) / 1000,
            input_tokens=review_data.get("token_count", 0) // 2,
            output_tokens=review_data.get("token_count", 0) // 2
        )

        processing_time = int((time.time() - start_time) * 1000)

        # Create response
        response = CodeReviewResponse(
            query_id=request.query_id,
            student_id=request.student_id,
            overall_rating=review_data["overall_rating"],
            feedback_items=review_data.get("feedback_items", []),
            summary=review_data["summary"],
            strengths=review_data.get("strengths", []),
            improvements=review_data.get("improvements", []),
            processing_time_ms=processing_time
        )

        # Publish response to Kafka
        envelope = KafkaMessageEnvelope(
            trace_id=request.query_id,
            event_type="code_reviewed",
            payload={
                "query_id": request.query_id,
                "student_id": request.student_id,
                "language": request.language,
                "response": response.model_dump()
            },
            metadata={
                "service_name": "code-review-agent",
                "processing_time_ms": processing_time
            }
        )

        kafka_publisher.publish(
            topic="agent-responses",
            message=envelope,
            key=request.student_id
        )

        metrics.track_kafka_message(topic="agent-responses", status="success")
        metrics.track_request(endpoint="/review", status="success")

        logger.info(
            f"Code review completed: query_id={request.query_id}, "
            f"rating={response.overall_rating}, processing_time={processing_time}ms"
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error reviewing code for query {request.query_id}: {e}", exc_info=True)
        metrics.track_request(endpoint="/review", status="error")
        raise HTTPException(status_code=500, detail=f"Code review failed: {str(e)}")


@router.get("/stats")
async def get_stats():
    """
    Get Code Review Agent statistics

    Returns basic stats about processed reviews.
    """
    return {
        "agent": "code-review-agent",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": ["/review", "/health", "/ready", "/stats"]
    }
