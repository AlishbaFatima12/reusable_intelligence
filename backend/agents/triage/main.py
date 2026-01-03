"""
Triage Agent - Main Application

FastAPI application for query routing and intent classification.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from backend.shared.logging_config import setup_logging
from backend.shared.health_checks import create_health_router
from backend.shared.metrics import MetricsCollector
from backend.agents.triage.routes import router as triage_router
from backend.agents.triage.config import config

# Setup logging
logger = setup_logging(service_name="triage-agent", log_level=config.log_level)

# Initialize metrics
metrics = MetricsCollector(agent_name="triage-agent")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager

    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting Triage Agent...")
    logger.info(f"Configuration: model={config.claude_model}, port={config.agent_port}")

    # Set agent metadata
    metrics.set_agent_info(
        version="1.0.0",
        metadata={
            "model": config.claude_model,
            "environment": config.environment
        }
    )

    yield

    # Shutdown
    logger.info("Shutting down Triage Agent...")


# Create FastAPI app
app = FastAPI(
    title="Triage Agent",
    description="Query routing and intent classification for LearnFlow platform",
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
app.include_router(triage_router, prefix="/api/v1", tags=["triage"])
app.include_router(create_health_router(), tags=["health"])

# Prometheus metrics endpoint
if config.enable_metrics:
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "triage-agent",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "analyze": "/api/v1/analyze",
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
