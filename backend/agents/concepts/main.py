"""
Concepts Agent - Main Application

FastAPI application for generating programming concept explanations.
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
from backend.agents.concepts.routes import router as concepts_router

# Setup logging
logger = setup_logging(service_name="concepts-agent", log_level=os.getenv("LOG_LEVEL", "INFO"))

# Initialize metrics
metrics = MetricsCollector(agent_name="concepts-agent")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager

    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting Concepts Agent...")
    logger.info(
        f"Configuration: model={os.getenv('OPENAI_MODEL', 'gpt-4o-mini')}, port=8002"
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
    # This would subscribe to concepts-queries topic
    # For now, the agent only handles direct HTTP requests

    yield

    # Shutdown
    logger.info("Shutting down Concepts Agent...")


# Create FastAPI app
app = FastAPI(
    title="Concepts Agent",
    description="Programming concept explanations for LearnFlow platform",
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
app.include_router(concepts_router, prefix="/api/v1", tags=["concepts"])
app.include_router(create_health_router(), tags=["health"])

# Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "concepts-agent",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "explain": "/api/v1/explain",
            "popular_concepts": "/api/v1/concepts/popular",
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
        port=8002,
        reload=True,
        log_level="info"
    )
