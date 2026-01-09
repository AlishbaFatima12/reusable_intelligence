"""
Exercise Generator - Main Application

FastAPI application for generating practice exercises.
"""

import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from backend.shared.logging_config import setup_logging
from backend.shared.health_checks import create_health_router
from backend.shared.metrics import MetricsCollector
from backend.agents.exercise.routes import router as exercise_router

# Setup logging
logger = setup_logging(service_name="exercise-generator-agent", log_level=os.getenv("LOG_LEVEL", "INFO"))

# Initialize metrics
metrics = MetricsCollector(agent_name="exercise-generator-agent")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager

    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting Exercise Generator Agent...")
    logger.info(
        f"Configuration: model={os.getenv('OPENAI_MODEL', 'gpt-4o-mini')}, port=8005"
    )

    # Set agent metadata
    metrics.set_agent_info(
        version="1.0.0",
        metadata={
            "model": os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
            "environment": os.getenv('ENVIRONMENT', 'development')
        }
    )

    # TODO: Start Kafka consumer in background
    # This would subscribe to exercise-queries topic
    # For now, the agent only handles direct HTTP requests

    yield

    # Shutdown
    logger.info("Shutting down Exercise Generator Agent...")


# Create FastAPI app
app = FastAPI(
    title="Exercise Generator",
    description="Practice exercise generation for LearnFlow platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(exercise_router, prefix="/api/v1", tags=["exercise"])
app.include_router(create_health_router(), tags=["health"])

# Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "exercise-generator-agent",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "generate": "/api/v1/generate",
            "exercises": "/api/v1/exercises/{topic}",
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
