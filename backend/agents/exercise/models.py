"""
Exercise Generator Pydantic Models

Request/Response models specific to the Exercise Generator Agent.
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class ExerciseGenerationRequest(BaseModel):
    """Request to generate practice exercises"""
    query_id: str = Field(..., description="Unique query identifier")
    student_id: str = Field(..., description="Student identifier")
    topic: str = Field(..., description="Topic for exercises (e.g., 'loops', 'functions')")
    difficulty_level: str = Field(default="beginner", description="Difficulty: beginner, intermediate, advanced")
    count: int = Field(default=3, ge=1, le=10, description="Number of exercises to generate")
    include_test_cases: bool = Field(default=True, description="Include test cases")
    mastery_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Current mastery score for difficulty scaling")


class TestCase(BaseModel):
    """Test case for an exercise"""
    input: str = Field(..., description="Input for the test case")
    expected_output: str = Field(..., description="Expected output")
    explanation: Optional[str] = Field(None, description="Why this test case is important")


class Exercise(BaseModel):
    """Individual practice exercise"""
    exercise_id: str = Field(..., description="Unique exercise identifier")
    title: str = Field(..., description="Exercise title")
    description: str = Field(..., description="Problem description")
    difficulty: str = Field(..., description="Difficulty level")
    starter_code: Optional[str] = Field(None, description="Starter code template")
    test_cases: List[TestCase] = Field(default_factory=list)
    hints: List[str] = Field(default_factory=list, description="Progressive hints")
    learning_objectives: List[str] = Field(default_factory=list)


class ExerciseGenerationResponse(BaseModel):
    """Response with generated exercises"""
    query_id: str
    student_id: str
    topic: str
    difficulty_level: str
    exercises: List[Exercise] = Field(default_factory=list)
    next_topic_suggestions: List[str] = Field(default_factory=list, description="Suggested next topics")
    processing_time_ms: int


class ExercisesListResponse(BaseModel):
    """Response for GET /exercises/{topic}"""
    topic: str
    available_exercises: List[Exercise] = Field(default_factory=list)
    difficulty_levels: List[str] = Field(default_factory=list)
