"""
Debug Agent API Routes

Endpoints for error diagnosis and debugging assistance.
"""

import logging
import time
from fastapi import APIRouter, HTTPException
from backend.agents.debug.models import DiagnosisRequest, DiagnosisResponse
from backend.agents.debug.services.debugger import Debugger
from backend.shared.claude_client import ClaudeClient
from backend.shared.kafka_client import KafkaPublisher
from backend.shared.models import KafkaMessageEnvelope
from backend.shared.metrics import MetricsCollector, track_latency
from backend.agents.debug.config import config

logger = logging.getLogger(__name__)

# Initialize dependencies
claude_client = ClaudeClient(
    model=config.claude_model,
    max_tokens=config.claude_max_tokens,
    rate_limit=config.claude_rate_limit,
    timeout=config.claude_timeout
)

debugger = Debugger(claude_client=claude_client)
kafka_publisher = KafkaPublisher(bootstrap_servers=config.kafka_bootstrap_servers)
metrics = MetricsCollector(agent_name="debug-agent")

router = APIRouter()


@router.post("/diagnose", response_model=DiagnosisResponse)
@track_latency(agent_name="debug-agent", endpoint="diagnose")
async def diagnose_error(request: DiagnosisRequest):
    """
    Diagnose error and provide debugging guidance

    Flow:
    1. Parse error message and stack trace
    2. Analyze using Claude API
    3. Extract diagnostic steps and suggestions
    4. Publish response to Kafka
    5. Return diagnosis
    """
    try:
        start_time = time.time()

        logger.info(
            f"Diagnosing error: query_id={request.query_id}, "
            f"language={request.language}"
        )

        # Diagnose error
        diagnosis_data = await debugger.diagnose_error(
            error_message=request.error_message,
            stack_trace=request.stack_trace,
            code_snippet=request.code_snippet,
            language=request.language
        )

        # Track Claude API metrics
        metrics.track_claude_call(
            model=config.claude_model,
            status="success",
            duration_seconds=diagnosis_data.get("processing_time_ms", 0) / 1000,
            input_tokens=0,  # Rough estimate
            output_tokens=0
        )

        processing_time = int((time.time() - start_time) * 1000)

        # Create response
        response = DiagnosisResponse(
            query_id=request.query_id,
            student_id=request.student_id,
            error_type=diagnosis_data["error_type"],
            root_cause=diagnosis_data["root_cause"],
            explanation=diagnosis_data["explanation"],
            diagnostic_steps=diagnosis_data.get("diagnostic_steps", []),
            suggested_fix=diagnosis_data.get("suggested_fix"),
            learning_resources=diagnosis_data.get("learning_resources", []),
            processing_time_ms=processing_time
        )

        # Publish response to Kafka
        envelope = KafkaMessageEnvelope(
            trace_id=request.query_id,
            event_type="error_diagnosed",
            payload={
                "query_id": request.query_id,
                "student_id": request.student_id,
                "language": request.language,
                "response": response.model_dump()
            },
            metadata={
                "service_name": "debug-agent",
                "processing_time_ms": processing_time
            }
        )

        kafka_publisher.publish(
            topic="agent-responses",
            message=envelope,
            key=request.student_id
        )

        metrics.track_kafka_message(topic="agent-responses", status="success")
        metrics.track_request(endpoint="/diagnose", status="success")

        logger.info(
            f"Error diagnosed: query_id={request.query_id}, "
            f"error_type={response.error_type}, processing_time={processing_time}ms"
        )

        return response

    except Exception as e:
        logger.error(f"Error diagnosing error for query {request.query_id}: {e}", exc_info=True)
        metrics.track_request(endpoint="/diagnose", status="error")
        raise HTTPException(status_code=500, detail=f"Error diagnosis failed: {str(e)}")


@router.get("/stats")
async def get_stats():
    """
    Get Debug Agent statistics

    Returns basic stats about processed diagnostics.
    """
    return {
        "agent": "debug-agent",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": ["/diagnose", "/health", "/ready", "/stats"]
    }
