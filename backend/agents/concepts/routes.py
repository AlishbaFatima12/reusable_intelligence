"""
Concepts Agent API Routes

Endpoints for generating concept explanations.
"""

import logging
import time
from fastapi import APIRouter, HTTPException
from backend.agents.concepts.models import (
    ConceptExplanationRequest, ConceptExplanationResponse,
    MCQGenerationRequest, MCQGenerationResponse, MCQ
)
from backend.agents.concepts.services.explainer import ConceptExplainer
from backend.agents.concepts.services.state_manager import ConceptStateManager
from backend.shared.openai_client import OpenAIClient
from backend.shared.kafka_client import KafkaPublisher
from backend.shared.models import KafkaMessageEnvelope
from backend.shared.metrics import MetricsCollector, track_latency
import os

logger = logging.getLogger(__name__)

# Initialize dependencies with OpenAI
openai_client = OpenAIClient(
    api_key=os.getenv("OPENAI_API_KEY"),
    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    max_tokens=4096,
    rate_limit=60,
    timeout=30
)

explainer = ConceptExplainer(claude_client=openai_client)
state_manager = ConceptStateManager()
kafka_publisher = KafkaPublisher(bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"))
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
        if True:  # Caching always enabled
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

        # Track OpenAI API metrics
        metrics.track_claude_call(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
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
        if True:  # Caching always enabled
            state_manager.cache_explanation(
                concept=request.concept,
                difficulty_level=request.difficulty_level,
                explanation=response
            )

        # Publish response to Kafka
        envelope = KafkaMessageEnvelope(
            trace_id=request.query_id,
            event_type="concept_explained",
            payload={
                "query_id": request.query_id,
                "student_id": request.student_id,
                "concept": request.concept,
                "response": response.model_dump()
            },
            metadata={
                "service_name": "concepts-agent",
                "processing_time_ms": processing_time
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


@router.post("/generate-mcqs", response_model=MCQGenerationResponse)
@track_latency(agent_name="concepts-agent", endpoint="generate_mcqs")
async def generate_mcqs(request: MCQGenerationRequest):
    """
    Generate new MCQs for a topic using AI

    Every call generates fresh questions - no caching.
    """
    try:
        logger.info(f"Generating {request.count} MCQs for topic={request.topic}, difficulty={request.difficulty}")

        # Map topic to readable name
        topic_names = {
            'python-basics': 'Python Basics',
            'variables-and-data-types': 'Variables and Data Types',
            'control-flow': 'Control Flow (if/else, loops)',
            'functions': 'Functions in Python',
            'data-structures': 'Data Structures (lists, dicts)'
        }
        topic_name = topic_names.get(request.topic, request.topic.replace('-', ' ').title())

        # Create prompt for MCQ generation
        prompt = f"""Generate exactly {request.count} multiple choice questions about {topic_name} in Python.

Difficulty level: {request.difficulty}

For each question, provide:
1. A clear question
2. Exactly 4 options (A, B, C, D)
3. The index of the correct answer (0=A, 1=B, 2=C, 3=D)

Return ONLY valid JSON in this exact format:
{{
    "questions": [
        {{
            "question": "What is...?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct": 0
        }}
    ]
}}

Make questions {request.difficulty} level - {'simple concepts' if request.difficulty == 'easy' else 'intermediate concepts with some edge cases' if request.difficulty == 'medium' else 'advanced concepts and tricky scenarios'}.
Generate UNIQUE questions - do not repeat common textbook questions."""

        # Call OpenAI API
        import json
        response = await openai_client.generate(
            prompt=prompt,
            system_prompt="You are a Python programming instructor creating quiz questions. Return ONLY valid JSON, no markdown."
        )

        # Parse response
        try:
            # Clean response - remove markdown code blocks if present
            response_text = response.strip()
            if response_text.startswith('```'):
                response_text = response_text.split('```')[1]
                if response_text.startswith('json'):
                    response_text = response_text[4:]
            response_text = response_text.strip()

            data = json.loads(response_text)
            questions = []
            for q in data.get('questions', [])[:request.count]:
                questions.append(MCQ(
                    question=q['question'],
                    options=q['options'][:4],
                    correct=q['correct']
                ))
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse MCQ response: {e}")
            # Fallback to static questions
            questions = get_fallback_mcqs(request.topic, request.count)

        metrics.track_request(endpoint="/generate-mcqs", status="success")

        return MCQGenerationResponse(
            topic=request.topic,
            difficulty=request.difficulty,
            questions=questions,
            generated_at=int(time.time())
        )

    except Exception as e:
        logger.error(f"Error generating MCQs: {e}", exc_info=True)
        metrics.track_request(endpoint="/generate-mcqs", status="error")
        # Return fallback questions instead of failing
        return MCQGenerationResponse(
            topic=request.topic,
            difficulty=request.difficulty,
            questions=get_fallback_mcqs(request.topic, request.count),
            generated_at=int(time.time())
        )


def get_fallback_mcqs(topic: str, count: int) -> list:
    """Fallback MCQs if AI generation fails"""
    import random

    fallback_db = {
        'python-basics': [
            MCQ(question="What is Python?", options=["A snake", "A programming language", "A database", "An operating system"], correct=1),
            MCQ(question="Which symbol starts a comment in Python?", options=["//", "/* */", "#", "<!--"], correct=2),
            MCQ(question="What does print() do?", options=["Reads input", "Outputs to console", "Creates a file", "Deletes data"], correct=1),
        ],
        'variables-and-data-types': [
            MCQ(question="Which is NOT a valid variable name?", options=["_var", "var1", "1var", "VAR"], correct=2),
            MCQ(question="What type is 3.14?", options=["int", "float", "str", "bool"], correct=1),
            MCQ(question="How to create a string?", options=["'hello'", "[hello]", "{hello}", "(hello)"], correct=0),
        ],
        'control-flow': [
            MCQ(question="Which keyword starts a conditional?", options=["for", "while", "if", "def"], correct=2),
            MCQ(question="What does 'break' do in a loop?", options=["Pauses", "Exits the loop", "Continues next", "Restarts"], correct=1),
            MCQ(question="Which is a loop keyword?", options=["if", "else", "for", "return"], correct=2),
        ],
        'functions': [
            MCQ(question="How to define a function?", options=["function f()", "def f():", "func f()", "define f()"], correct=1),
            MCQ(question="What does return do?", options=["Prints value", "Sends back value", "Deletes function", "Creates loop"], correct=1),
            MCQ(question="What are parameters?", options=["Return values", "Input values", "Local variables", "Global variables"], correct=1),
        ],
        'data-structures': [
            MCQ(question="How to create an empty list?", options=["{}", "[]", "()", "<>"], correct=1),
            MCQ(question="Which adds to a list?", options=["add()", "append()", "insert()", "push()"], correct=1),
            MCQ(question="What is a dictionary key?", options=["Always a number", "Always a string", "Any immutable type", "Any type"], correct=2),
        ],
    }

    questions = fallback_db.get(topic, fallback_db['python-basics'])
    random.shuffle(questions)
    return questions[:count]


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
