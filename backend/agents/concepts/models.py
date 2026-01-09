"""
Concepts Agent Pydantic Models

Request/Response models specific to the Concepts Agent.
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class ConceptExplanationRequest(BaseModel):
    """Request to explain a programming concept"""
    query_id: str = Field(..., description="Unique query identifier")
    student_id: str = Field(..., description="Student identifier")
    concept: str = Field(..., min_length=1, max_length=200, description="Concept to explain")
    difficulty_level: Optional[str] = Field(default="beginner", description="Difficulty level: beginner, intermediate, advanced")
    include_examples: bool = Field(default=True, description="Include code examples")
    include_visualization: bool = Field(default=True, description="Include ASCII visualizations")


class CodeExample(BaseModel):
    """Code example for concept explanation"""
    title: str = Field(..., description="Example title")
    code: str = Field(..., description="Python code")
    explanation: str = Field(..., description="What this example demonstrates")


class ConceptExplanationResponse(BaseModel):
    """Response containing concept explanation"""
    query_id: str
    student_id: str
    concept: str
    explanation: str = Field(..., description="Clear explanation of the concept")
    code_examples: List[CodeExample] = Field(default_factory=list)
    visualization: Optional[str] = Field(None, description="ASCII visualization or diagram")
    key_points: List[str] = Field(default_factory=list, description="Key takeaways")
    common_mistakes: List[str] = Field(default_factory=list, description="Common pitfalls to avoid")
    next_steps: Optional[str] = Field(None, description="Suggested next learning steps")
    processing_time_ms: int


class CachedExplanation(BaseModel):
    """Cached explanation stored in Dapr state store"""
    concept: str
    difficulty_level: str
    explanation: ConceptExplanationResponse
    cache_timestamp: int = Field(..., description="Unix timestamp when cached")
    hit_count: int = Field(default=1, description="Number of times this cache was hit")


# MCQ Generation Models
class MCQOption(BaseModel):
    """Single MCQ option"""
    text: str = Field(..., description="Option text")
    is_correct: bool = Field(default=False, description="Whether this is the correct answer")


class MCQ(BaseModel):
    """Single multiple choice question"""
    question: str = Field(..., description="The question text")
    options: List[str] = Field(..., min_length=4, max_length=4, description="Four answer options")
    correct: int = Field(..., ge=0, le=3, description="Index of correct answer (0-3)")
    explanation: Optional[str] = Field(None, description="Why this answer is correct")


class MCQGenerationRequest(BaseModel):
    """Request to generate MCQs"""
    topic: str = Field(..., description="Topic for MCQs (e.g., 'python-basics')")
    difficulty: str = Field(default="easy", description="Difficulty: easy, medium, hard")
    count: int = Field(default=3, ge=1, le=10, description="Number of questions to generate")
    student_id: Optional[str] = Field(None, description="Student ID for personalization")


class MCQGenerationResponse(BaseModel):
    """Response containing generated MCQs"""
    topic: str
    difficulty: str
    questions: List[MCQ]
    generated_at: int = Field(..., description="Unix timestamp")
