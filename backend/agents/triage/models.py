"""
Triage Agent Pydantic Models

Request/Response models specific to the Triage Agent.
"""

from typing import Optional, List
from pydantic import BaseModel, Field
from backend.shared.models import IntentType, StudentQuery


class QueryAnalysisRequest(BaseModel):
    """Request to analyze a student query"""
    query_id: str = Field(..., description="Unique query identifier")
    student_id: str = Field(..., description="Student identifier")
    query_text: str = Field(..., min_length=1, max_length=5000, description="Student's question")
    code_snippet: Optional[str] = Field(None, max_length=10000, description="Optional code snippet")
    learning_context: Optional[str] = Field(None, description="Current learning context (topic, lesson)")


class QueryAnalysisResponse(BaseModel):
    """Result of query analysis"""
    query_id: str
    detected_intent: IntentType
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Classification confidence")
    routed_to_agent: str = Field(..., description="Target agent name")
    extracted_entities: Optional[dict] = Field(default_factory=dict, description="Extracted topics, concepts")
    reasoning: Optional[str] = Field(None, description="Why this routing decision was made")
    processing_time_ms: int


class RoutingDecision(BaseModel):
    """Routing decision published to Kafka"""
    query_id: str
    student_id: str
    detected_intent: IntentType
    routed_to_agent: str
    confidence_score: float
    target_topic: str = Field(..., description="Kafka topic to publish to")
    original_query: StudentQuery
