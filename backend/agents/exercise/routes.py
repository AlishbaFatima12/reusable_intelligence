"""
Exercise Generator API Routes

Endpoints for generating practice exercises.
"""

import logging
import time
from fastapi import APIRouter, HTTPException, Path
from backend.agents.exercise.models import (
    ExerciseGenerationRequest,
    ExerciseGenerationResponse,
    ExercisesListResponse
)
from backend.agents.exercise.services.generator import ExerciseGenerator
from backend.shared.openai_client import OpenAIClient
from backend.shared.kafka_client import KafkaPublisher
from backend.shared.models import KafkaMessageEnvelope
from backend.shared.metrics import MetricsCollector, track_latency
import os

logger = logging.getLogger(__name__)

# Initialize dependencies
openai_client = OpenAIClient(
    api_key=os.getenv("OPENAI_API_KEY"),
    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    max_tokens=4096,
    rate_limit=60,
    timeout=30
)

generator = ExerciseGenerator(claude_client=openai_client)
kafka_publisher = KafkaPublisher(bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"))
metrics = MetricsCollector(agent_name="exercise-generator-agent")

router = APIRouter()

# In-memory cache for generated exercises (for demo purposes)
# In production, this would use Dapr state store
exercise_cache = {}


@router.post("/generate", response_model=ExerciseGenerationResponse)
@track_latency(agent_name="exercise-generator-agent", endpoint="generate")
async def generate_exercises(request: ExerciseGenerationRequest):
    """
    Generate practice exercises for a topic

    Flow:
    1. Determine difficulty based on mastery score
    2. Generate exercises using Claude API
    3. Cache exercises for future retrieval
    4. Publish response to Kafka
    5. Return exercises
    """
    try:
        start_time = time.time()

        logger.info(
            f"Generating exercises: query_id={request.query_id}, "
            f"topic={request.topic}, difficulty={request.difficulty_level}, count={request.count}"
        )

        # Generate exercises
        result = await generator.generate_exercises(
            topic=request.topic,
            difficulty_level=request.difficulty_level,
            count=request.count,
            include_test_cases=request.include_test_cases,
            mastery_score=request.mastery_score
        )

        # Track OpenAI API metrics
        metrics.track_claude_call(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            status="success",
            duration_seconds=0,  # TODO: track actual time
            input_tokens=0,
            output_tokens=0
        )

        processing_time = int((time.time() - start_time) * 1000)

        # Create response
        response = ExerciseGenerationResponse(
            query_id=request.query_id,
            student_id=request.student_id,
            topic=request.topic,
            difficulty_level=result.get("recommended_difficulty", request.difficulty_level),
            exercises=result["exercises"],
            next_topic_suggestions=result["next_topic_suggestions"],
            processing_time_ms=processing_time
        )

        # Cache exercises
        cache_key = f"{request.topic}:{response.difficulty_level}"
        exercise_cache[cache_key] = response.exercises

        # Publish response to Kafka
        envelope = KafkaMessageEnvelope(
            trace_id=request.query_id,
            event_type="exercises_generated",
            payload={
                "query_id": request.query_id,
                "student_id": request.student_id,
                "topic": request.topic,
                "response": response.model_dump()
            },
            metadata={
                "service_name": "exercise-generator-agent",
                "processing_time_ms": processing_time
            }
        )

        kafka_publisher.publish(
            topic="agent-responses",
            message=envelope,
            key=request.student_id
        )

        metrics.track_kafka_message(topic="agent-responses", status="success")
        metrics.track_request(endpoint="/generate", status="success")

        logger.info(
            f"Exercises generated: query_id={request.query_id}, "
            f"count={len(response.exercises)}, processing_time={processing_time}ms"
        )

        return response

    except Exception as e:
        logger.error(f"Error generating exercises for query {request.query_id}: {e}", exc_info=True)
        metrics.track_request(endpoint="/generate", status="error")
        raise HTTPException(status_code=500, detail=f"Exercise generation failed: {str(e)}")


@router.get("/exercises/{topic}", response_model=ExercisesListResponse)
@track_latency(agent_name="exercise-generator-agent", endpoint="exercises")
async def get_exercises(
    topic: str = Path(..., description="Topic to get exercises for")
):
    """
    Get available exercises for a topic

    Returns cached exercises if available.
    """
    try:
        logger.info(f"Fetching exercises for topic: {topic}")

        # Check cache for all difficulty levels
        available_exercises = []
        difficulty_levels = []

        for difficulty in ["beginner", "intermediate", "advanced"]:
            cache_key = f"{topic}:{difficulty}"
            if cache_key in exercise_cache:
                exercises = exercise_cache[cache_key]
                available_exercises.extend(exercises)
                difficulty_levels.append(difficulty)

        metrics.track_request(endpoint="/exercises", status="success")

        return ExercisesListResponse(
            topic=topic,
            available_exercises=available_exercises,
            difficulty_levels=difficulty_levels
        )

    except Exception as e:
        logger.error(f"Error fetching exercises for topic {topic}: {e}", exc_info=True)
        metrics.track_request(endpoint="/exercises", status="error")
        raise HTTPException(status_code=500, detail=f"Failed to fetch exercises: {str(e)}")


@router.get("/stats")
async def get_stats():
    """
    Get Exercise Generator statistics

    Returns basic stats about generated exercises.
    """
    total_exercises = sum(len(exercises) for exercises in exercise_cache.values())

    return {
        "agent": "exercise-generator-agent",
        "version": "1.0.0",
        "status": "operational",
        "cached_topics": len(exercise_cache),
        "total_cached_exercises": total_exercises,
        "endpoints": ["/generate", "/exercises/{topic}", "/health", "/ready", "/stats"]
    }
