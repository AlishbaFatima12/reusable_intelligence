"""
Concepts Agent - Main Application

FastAPI application for generating programming concept explanations.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from backend.shared.logging_config import setup_logging
from backend.shared.health_checks import create_health_router
from backend.shared.metrics import MetricsCollector
from backend.agents.concepts.routes import router as concepts_router
from backend.agents.concepts.config import config

# Setup logging
logger = setup_logging(service_name="concepts-agent", log_level=config.log_level)

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
        f"Configuration: model={config.claude_model}, port={config.agent_port}, "
        f"caching={config.enable_caching}"
    )

    # Set agent metadata
    metrics.set_agent_info(
        version="1.0.0",
        metadata={
            "model": config.claude_model,
            "environment": config.environment,
            "caching_enabled": str(config.enable_caching)
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
    allow_origins=["*"] if config.is_development else ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(concepts_router, prefix="/api/v1", tags=["concepts"])
app.include_router(create_health_router(), tags=["health"])

# Prometheus metrics endpoint
if config.enable_metrics:
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
        port=config.agent_port,
        reload=config.is_development,
        log_level=config.log_level.lower()
    )
