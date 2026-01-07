"""
Debug Agent Pydantic Models

Request/Response models specific to the Debug Agent.
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class DiagnosisRequest(BaseModel):
    """Request to diagnose an error"""
    query_id: str = Field(..., description="Unique query identifier")
    student_id: str = Field(..., description="Student identifier")
    error_message: str = Field(..., description="Error message or exception text")
    stack_trace: Optional[str] = Field(None, description="Full stack trace")
    code_snippet: Optional[str] = Field(None, max_length=5000, description="Code that caused the error")
    language: str = Field(default="python", description="Programming language")


class DiagnosticStep(BaseModel):
    """Individual diagnostic step"""
    step_number: int
    description: str = Field(..., description="What to check or try")
    reason: str = Field(..., description="Why this step is important")
    example: Optional[str] = Field(None, description="Example code or command")


class DiagnosisResponse(BaseModel):
    """Error diagnosis and debugging suggestions"""
    query_id: str
    student_id: str
    error_type: str = Field(..., description="Classified error type: syntax, runtime, logic, etc.")
    root_cause: str = Field(..., description="Likely root cause of the error")
    explanation: str = Field(..., description="Detailed explanation of what went wrong")
    diagnostic_steps: List[DiagnosticStep] = Field(default_factory=list)
    suggested_fix: Optional[str] = Field(None, description="Suggested code fix")
    learning_resources: List[str] = Field(default_factory=list, description="Links to relevant documentation")
    processing_time_ms: int
