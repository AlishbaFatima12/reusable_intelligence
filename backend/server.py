"""
Combined server for all LearnFlow agents.
Single entry point for cloud deployment (Render, Railway, etc.)
"""

import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Import agent routers
from agents.triage.routes import router as triage_router
from agents.concepts.routes import router as concepts_router
from agents.code_review.routes import router as code_review_router
from agents.debug.routes import router as debug_router
from agents.exercise.routes import router as exercise_router
from agents.progress.routes import router as progress_router

app = FastAPI(
    title="LearnFlow AI Agents",
    description="Combined API for all LearnFlow learning agents",
    version="1.0.0"
)

# CORS - allow all origins for demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/")
async def root():
    return {"status": "healthy", "service": "LearnFlow AI Agents"}

@app.get("/health")
async def health():
    return {"status": "ok", "agents": ["triage", "concepts", "code_review", "debug", "exercise", "progress"]}

# Mount agent routers with prefixes
app.include_router(triage_router, prefix="/api/v1/triage", tags=["Triage"])
app.include_router(concepts_router, prefix="/api/v1/concepts", tags=["Concepts"])
app.include_router(code_review_router, prefix="/api/v1/code-review", tags=["Code Review"])
app.include_router(debug_router, prefix="/api/v1/debug", tags=["Debug"])
app.include_router(exercise_router, prefix="/api/v1/exercise", tags=["Exercise"])
app.include_router(progress_router, prefix="/api/v1/progress", tags=["Progress"])

# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "detail": "Internal server error"}
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
