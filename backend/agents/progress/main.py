"""
Progress Tracker Agent - Main Application

FastAPI application for tracking student learning progress and mastery.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from backend.shared.logging_config import setup_logging
from backend.shared.health_checks import create_health_router
from backend.shared.metrics import MetricsCollector
from backend.agents.progress.routes import router as progress_router
from backend.agents.progress.config import config

# Setup logging
logger = setup_logging(service_name="progress-tracker-agent", log_level=config.log_level)

# Initialize metrics
metrics = MetricsCollector(agent_name="progress-tracker-agent")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager

    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting Progress Tracker Agent...")
    logger.info(
        f"Configuration: model={config.claude_model}, port={config.agent_port}, "
        f"mastery_threshold={config.mastery_threshold}"
    )

    # Set agent metadata
    metrics.set_agent_info(
        version="1.0.0",
        metadata={
            "model": config.claude_model,
            "environment": config.environment,
            "mastery_threshold": str(config.mastery_threshold)
        }
    )

    # TODO: Start Kafka consumer in background
    # This would subscribe to agent-responses topic to auto-update progress
    # For now, the agent only handles direct HTTP requests

    yield

    # Shutdown
    logger.info("Shutting down Progress Tracker Agent...")


# Create FastAPI app
app = FastAPI(
    title="Progress Tracker Agent",
    description="Learning analytics and mastery tracking for LearnFlow platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if config.is_development else ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(progress_router, prefix="/api/v1", tags=["progress"])
app.include_router(create_health_router(), tags=["health"])

# Prometheus metrics endpoint
if config.enable_metrics:
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "progress-tracker-agent",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "get_mastery": "/api/v1/mastery/{student_id}",
            "update_mastery": "POST /api/v1/mastery/{student_id}",
            "insights": "/api/v1/insights/{student_id}",
            "struggle_detection": "POST /api/v1/struggle-detection",
            "stats": "/api/v1/stats",
            "health": "/health",
            "ready": "/ready",
            "metrics": "/metrics"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=config.agent_port,
        reload=config.is_development,
        log_level=config.log_level.lower()
    )
