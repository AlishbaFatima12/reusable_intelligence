"""
Prometheus metrics helpers for agent observability.

Provides standardized metrics for:
- Request counters (by agent, endpoint, status)
- Latency histograms
- Error rates
- Active requests and queue sizes
"""

import logging
import time
from typing import Optional, Dict, Any
from functools import wraps
from prometheus_client import Counter, Histogram, Gauge, Info

logger = logging.getLogger(__name__)


# Request metrics
REQUEST_COUNT = Counter(
    'agent_requests_total',
    'Total requests processed by agent',
    ['agent_name', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'agent_request_duration_seconds',
    'Request processing time in seconds',
    ['agent_name', 'endpoint'],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0)
)

# Agent-specific metrics
ACTIVE_REQUESTS = Gauge(
    'agent_active_requests',
    'Number of requests currently being processed',
    ['agent_name']
)

KAFKA_MESSAGES_PROCESSED = Counter(
    'agent_kafka_messages_total',
    'Total Kafka messages consumed',
    ['agent_name', 'topic', 'status']
)

CLAUDE_API_CALLS = Counter(
    'claude_api_calls_total',
    'Total Claude API calls',
    ['agent_name', 'model', 'status']
)

CLAUDE_API_LATENCY = Histogram(
    'claude_api_duration_seconds',
    'Claude API call duration',
    ['agent_name', 'model'],
    buckets=(0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0)
)

CLAUDE_TOKENS_USED = Counter(
    'claude_tokens_total',
    'Total tokens used in Claude API calls',
    ['agent_name', 'model', 'token_type']
)

# State management metrics
STATE_OPERATIONS = Counter(
    'state_operations_total',
    'Total state store operations',
    ['agent_name', 'operation', 'status']
)

# Queue metrics
QUEUE_SIZE = Gauge(
    'message_queue_size',
    'Current size of message queue',
    ['agent_name', 'queue_type']
)

# Agent health
AGENT_INFO = Info(
    'agent_info',
    'Agent metadata and version information'
)


class MetricsCollector:
    """Centralized metrics collection for agents"""

    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        logger.info(f"Initialized metrics collector for {agent_name}")

    def track_request(self, endpoint: str, status: str = "success"):
        """Track HTTP request"""
        REQUEST_COUNT.labels(
            agent_name=self.agent_name,
            endpoint=endpoint,
            status=status
        ).inc()

    def track_kafka_message(self, topic: str, status: str = "success"):
        """Track Kafka message processing"""
        KAFKA_MESSAGES_PROCESSED.labels(
            agent_name=self.agent_name,
            topic=topic,
            status=status
        ).inc()

    def track_claude_call(
        self,
        model: str,
        status: str,
        duration_seconds: float,
        input_tokens: int,
        output_tokens: int
    ):
        """Track Claude API call with full metrics"""
        CLAUDE_API_CALLS.labels(
            agent_name=self.agent_name,
            model=model,
            status=status
        ).inc()

        CLAUDE_API_LATENCY.labels(
            agent_name=self.agent_name,
            model=model
        ).observe(duration_seconds)

        CLAUDE_TOKENS_USED.labels(
            agent_name=self.agent_name,
            model=model,
            token_type="input"
        ).inc(input_tokens)

        CLAUDE_TOKENS_USED.labels(
            agent_name=self.agent_name,
            model=model,
            token_type="output"
        ).inc(output_tokens)

    def track_state_operation(self, operation: str, status: str = "success"):
        """Track state store operation"""
        STATE_OPERATIONS.labels(
            agent_name=self.agent_name,
            operation=operation,
            status=status
        ).inc()

    def set_queue_size(self, queue_type: str, size: int):
        """Update queue size gauge"""
        QUEUE_SIZE.labels(
            agent_name=self.agent_name,
            queue_type=queue_type
        ).set(size)

    def set_agent_info(self, version: str, metadata: Optional[Dict[str, str]] = None):
        """Set agent metadata"""
        info = {
            "agent_name": self.agent_name,
            "version": version
        }
        if metadata:
            info.update(metadata)
        AGENT_INFO.info(info)


def track_latency(agent_name: str, endpoint: str):
    """Decorator to track function latency"""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            ACTIVE_REQUESTS.labels(agent_name=agent_name).inc()
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                REQUEST_LATENCY.labels(
                    agent_name=agent_name,
                    endpoint=endpoint
                ).observe(duration)
                return result
            finally:
                ACTIVE_REQUESTS.labels(agent_name=agent_name).dec()

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            ACTIVE_REQUESTS.labels(agent_name=agent_name).inc()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                REQUEST_LATENCY.labels(
                    agent_name=agent_name,
                    endpoint=endpoint
                ).observe(duration)
                return result
            finally:
                ACTIVE_REQUESTS.labels(agent_name=agent_name).dec()

        # Return appropriate wrapper based on function type
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator
