"""
Code Review Agent Pydantic Models

Request/Response models specific to the Code Review Agent.
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class CodeReviewRequest(BaseModel):
    """Request to review student code"""
    query_id: str = Field(..., description="Unique query identifier")
    student_id: str = Field(..., description="Student identifier")
    code: str = Field(..., min_length=1, max_length=10000, description="Code to review")
    language: str = Field(default="python", description="Programming language")
    context: Optional[str] = Field(None, description="What the code is supposed to do")


class CodeFeedback(BaseModel):
    """Individual feedback item"""
    category: str = Field(..., description="Category: style, correctness, efficiency, best_practice")
    severity: str = Field(..., description="Severity: info, warning, error")
    line_number: Optional[int] = Field(None, description="Line number (if applicable)")
    message: str = Field(..., description="Feedback message")
    suggestion: Optional[str] = Field(None, description="Suggested fix or improvement")


class CodeReviewResponse(BaseModel):
    """Code review feedback"""
    query_id: str
    student_id: str
    overall_rating: str = Field(..., description="Overall code quality: excellent, good, needs_improvement, poor")
    feedback_items: List[CodeFeedback] = Field(default_factory=list)
    summary: str = Field(..., description="Overall assessment summary")
    strengths: List[str] = Field(default_factory=list, description="What the student did well")
    improvements: List[str] = Field(default_factory=list, description="Areas for improvement")
    processing_time_ms: int
