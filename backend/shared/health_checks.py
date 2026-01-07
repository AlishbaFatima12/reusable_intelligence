"""Health and readiness check handlers"""

import time
from fastapi import APIRouter
from .models import HealthResponse, ReadinessResponse

start_time = time.time()


def create_health_router() -> APIRouter:
    """Create health check router"""
    router = APIRouter()

    @router.get("/health", response_model=HealthResponse)
    async def health_check():
        """Liveness probe - is service running?"""
        uptime = int(time.time() - start_time)
        return HealthResponse(status="healthy", uptime_seconds=uptime)

    @router.get("/ready", response_model=ReadinessResponse)
    async def readiness_check():
        """Readiness probe - can service accept traffic?"""
        # TODO: Check Kafka and Dapr connectivity
        return ReadinessResponse(
            ready=True,
            kafka_connected=True,
            dapr_connected=True
        )

    return router
