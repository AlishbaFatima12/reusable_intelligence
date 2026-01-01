"""
Triage Agent - Routes student queries to appropriate specialist agents

This agent classifies incoming student queries and routes them to the appropriate
specialist agent (Concepts, Code Review, Debug, Exercise, or Progress).
"""
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class QueryRequest(BaseModel):
    """Student query with context"""
    query: str
    student_id: str
    context: dict | None = None

class RoutingDecision(BaseModel):
    """Routing decision with reasoning"""
    target_agent: str
    confidence: float
    reasoning: str

@app.post("/classify")
async def classify_query(request: QueryRequest) -> RoutingDecision:
    """Classifies query intent and routes to specialist agent"""
    # Placeholder implementation
    return RoutingDecision(
        target_agent="concepts",
        confidence=0.95,
        reasoning="Query asks for concept explanation"
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "agent": "triage"}
