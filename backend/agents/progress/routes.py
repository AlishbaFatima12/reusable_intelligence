"""
Progress Tracker Agent API Routes

Endpoints for tracking student progress and mastery.
"""

import logging
import time
from fastapi import APIRouter, HTTPException
from backend.agents.progress.models import (
    MasteryRequest,
    MasteryResponse,
    StruggleDetectionRequest,
    StruggleDetectionResponse
)
from backend.agents.progress.services.tracker import ProgressTracker
from backend.agents.progress.services.analytics import LearningAnalytics
from backend.agents.progress.services.state_manager import ProgressStateManager
from backend.shared.claude_client import ClaudeClient
from backend.shared.kafka_client import KafkaPublisher
from backend.shared.models import KafkaMessageEnvelope
from backend.shared.metrics import MetricsCollector, track_latency
from backend.agents.progress.config import config

logger = logging.getLogger(__name__)

# Initialize dependencies
claude_client = ClaudeClient(
    model=config.claude_model,
    max_tokens=config.claude_max_tokens,
    rate_limit=config.claude_rate_limit,
    timeout=config.claude_timeout
)

tracker = ProgressTracker()
analytics = LearningAnalytics(claude_client=claude_client)
state_manager = ProgressStateManager()
kafka_publisher = KafkaPublisher(bootstrap_servers=config.kafka_bootstrap_servers)
metrics = MetricsCollector(agent_name="progress-tracker-agent")

router = APIRouter()


@router.get("/mastery/{student_id}", response_model=MasteryResponse)
@track_latency(agent_name="progress-tracker-agent", endpoint="get_mastery")
async def get_mastery(student_id: str):
    """
    Get student's current mastery levels

    Returns overall mastery, topic breakdown, and recommendations.
    """
    try:
        logger.info(f"Retrieving mastery for student: {student_id}")

        # Get student progress state
        student_state = state_manager.get_student_progress(student_id)

        # Get next recommended topic
        next_topic = tracker.get_next_recommended_topic(student_state)

        # Track request
        metrics.track_request(endpoint="/mastery", status="success")

        return MasteryResponse(
            student_id=student_id,
            overall_mastery=student_state.progress.overall_mastery,
            topic_mastery=student_state.progress.topic_mastery,
            struggling_topics=student_state.struggling_topics,
            next_recommended_topic=next_topic
        )

    except Exception as e:
        logger.error(f"Error retrieving mastery for {student_id}: {e}", exc_info=True)
        metrics.track_request(endpoint="/mastery", status="error")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve mastery: {str(e)}")


@router.post("/mastery/{student_id}", response_model=MasteryResponse)
@track_latency(agent_name="progress-tracker-agent", endpoint="update_mastery")
async def update_mastery(student_id: str, request: MasteryRequest):
    """
    Update student's mastery for a topic

    Flow:
    1. Retrieve current progress state
    2. Update topic mastery based on interaction
    3. Save updated state
    4. Publish progress update to Kafka
    5. Return updated mastery
    """
    try:
        logger.info(
            f"Updating mastery: student={student_id}, topic={request.topic}, "
            f"type={request.interaction_type}, success={request.success}"
        )

        # Get current progress state
        student_state = state_manager.get_student_progress(student_id)

        # Store old mastery for comparison
        old_overall_mastery = student_state.progress.overall_mastery

        # Update mastery
        student_state = tracker.update_topic_mastery(
            student_state=student_state,
            topic=request.topic,
            interaction_type=request.interaction_type,
            success=request.success
        )

        # Update query counts
        student_state.total_queries += 1
        if request.success:
            student_state.total_successful_queries += 1

        # Save updated state
        state_manager.save_student_progress(student_state)

        # Publish progress update to Kafka
        from uuid import uuid4
        envelope = KafkaMessageEnvelope(
            trace_id=str(uuid4()),
            event_type="progress_updated",
            payload={
                "student_id": student_id,
                "topic": request.topic,
                "old_mastery": old_overall_mastery,
                "new_mastery": student_state.progress.overall_mastery,
                "struggling_topics": student_state.struggling_topics
            },
            metadata={"service_name": "progress-tracker-agent"}
        )

        kafka_publisher.publish(
            topic="mastery-updates",
            message=envelope,
            key=student_id
        )

        metrics.track_kafka_message(topic="mastery-updates", status="success")
        metrics.track_request(endpoint="/mastery", status="success")

        # Get next recommended topic
        next_topic = tracker.get_next_recommended_topic(student_state)

        return MasteryResponse(
            student_id=student_id,
            overall_mastery=student_state.progress.overall_mastery,
            topic_mastery=student_state.progress.topic_mastery,
            struggling_topics=student_state.struggling_topics,
            next_recommended_topic=next_topic
        )

    except Exception as e:
        logger.error(f"Error updating mastery for {student_id}: {e}", exc_info=True)
        metrics.track_request(endpoint="/mastery", status="error")
        raise HTTPException(status_code=500, detail=f"Failed to update mastery: {str(e)}")


@router.get("/insights/{student_id}")
@track_latency(agent_name="progress-tracker-agent", endpoint="get_insights")
async def get_insights(student_id: str):
    """
    Get personalized learning insights for a student

    Uses Claude API to analyze progress and generate recommendations.
    """
    try:
        logger.info(f"Generating insights for student: {student_id}")

        # Get student progress state
        student_state = state_manager.get_student_progress(student_id)

        # Generate insights using Claude API
        insights = await analytics.generate_insights(student_state)

        metrics.track_request(endpoint="/insights", status="success")

        return {
            "student_id": student_id,
            "insights": [insight.model_dump() for insight in insights],
            "generated_at": int(time.time())
        }

    except Exception as e:
        logger.error(f"Error generating insights for {student_id}: {e}", exc_info=True)
        metrics.track_request(endpoint="/insights", status="error")
        raise HTTPException(status_code=500, detail=f"Failed to generate insights: {str(e)}")


@router.post("/struggle-detection", response_model=StruggleDetectionResponse)
@track_latency(agent_name="progress-tracker-agent", endpoint="detect_struggle")
async def detect_struggle(request: StruggleDetectionRequest):
    """
    Detect if a student is struggling based on recent activity

    Uses Claude API to analyze query patterns and error frequency.
    """
    try:
        logger.info(f"Detecting struggle for student: {request.student_id}")

        # Detect struggle using Claude API
        struggle_data = await analytics.detect_struggle(
            student_id=request.student_id,
            recent_queries=request.recent_queries,
            recent_errors=request.recent_errors
        )

        metrics.track_request(endpoint="/struggle-detection", status="success")

        # If struggling, publish alert to Kafka
        if struggle_data.get("is_struggling", False):
            from uuid import uuid4
            envelope = KafkaMessageEnvelope(
                trace_id=str(uuid4()),
                event_type="student_struggling",
                payload={
                    "student_id": request.student_id,
                    "confidence": struggle_data.get("confidence", 0.0),
                    "indicators": struggle_data.get("struggle_indicators", []),
                    "interventions": struggle_data.get("suggested_interventions", [])
                },
                metadata={"service_name": "progress-tracker-agent"}
            )

            kafka_publisher.publish(
                topic="student-struggle",
                message=envelope,
                key=request.student_id
            )

            logger.warning(f"Student {request.student_id} is struggling - alert published")

        return StruggleDetectionResponse(
            student_id=request.student_id,
            is_struggling=struggle_data.get("is_struggling", False),
            confidence=struggle_data.get("confidence", 0.0),
            struggle_indicators=struggle_data.get("struggle_indicators", []),
            suggested_interventions=struggle_data.get("suggested_interventions", [])
        )

    except Exception as e:
        logger.error(f"Error detecting struggle for {request.student_id}: {e}", exc_info=True)
        metrics.track_request(endpoint="/struggle-detection", status="error")
        raise HTTPException(status_code=500, detail=f"Struggle detection failed: {str(e)}")


@router.get("/stats")
async def get_stats():
    """
    Get Progress Tracker Agent statistics

    Returns basic stats about tracked students.
    """
    return {
        "agent": "progress-tracker-agent",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": [
            "/mastery/{student_id}",
            "/insights/{student_id}",
            "/struggle-detection",
            "/health",
            "/ready",
            "/stats"
        ]
    }
