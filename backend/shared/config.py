"""
Environment variable configuration using Pydantic Settings.

Provides type-safe, validated configuration loading for all agents.
Supports .env files and environment variables.
"""

import os
from typing import Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AgentConfig(BaseSettings):
    """Base configuration for all agents"""

    model_config = SettingsConfigDict(
        env_file=['D:/reuse-skills/.env', 'D:/reuse-skills/backend/.env', '.env'],
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore'
    )

    # Environment
    environment: str = Field(default="development", description="Environment: development, staging, production")
    debug: bool = Field(default=False, description="Enable debug mode")
    log_level: str = Field(default="INFO", description="Logging level")

    # Claude API Configuration
    anthropic_api_key: str = Field(..., description="Anthropic API key for Claude")
    claude_model: str = Field(default="claude-3-haiku-20240307", description="Claude model to use")
    claude_max_tokens: int = Field(default=4096, description="Max tokens for Claude responses")
    claude_timeout: int = Field(default=30, description="Claude API timeout in seconds")
    claude_rate_limit: int = Field(default=60, description="Claude API requests per minute")

    # Kafka Configuration
    kafka_bootstrap_servers: str = Field(default="localhost:9092", description="Kafka bootstrap servers")
    kafka_group_id_prefix: str = Field(default="learnflow", description="Kafka consumer group ID prefix")
    kafka_auto_offset_reset: str = Field(default="latest", description="Kafka auto offset reset")

    # PostgreSQL Configuration
    postgres_host: str = Field(default="localhost", description="PostgreSQL host")
    postgres_port: int = Field(default=5432, description="PostgreSQL port")
    postgres_db: str = Field(default="learnflow_db", description="PostgreSQL database name")
    postgres_user: str = Field(default="learnflow_user", description="PostgreSQL username")
    postgres_password: str = Field(default="learnflow_pass", description="PostgreSQL password")

    # Dapr Configuration
    dapr_http_port: int = Field(default=3500, description="Dapr HTTP port")
    dapr_grpc_port: int = Field(default=50001, description="Dapr gRPC port")
    dapr_state_store_name: str = Field(default="statestore", description="Dapr state store component name")
    dapr_pubsub_name: str = Field(default="kafka-pubsub", description="Dapr pub/sub component name")

    # Agent Ports (for direct HTTP calls if needed)
    triage_port: int = Field(default=8001, description="Triage Agent port")
    concepts_port: int = Field(default=8002, description="Concepts Agent port")
    code_review_port: int = Field(default=8003, description="Code Review Agent port")
    debug_port: int = Field(default=8004, description="Debug Agent port")
    exercise_port: int = Field(default=8005, description="Exercise Generator port")
    progress_port: int = Field(default=8006, description="Progress Tracker port")

    # Observability
    enable_metrics: bool = Field(default=True, description="Enable Prometheus metrics")
    metrics_port: int = Field(default=9090, description="Prometheus metrics port")
    enable_tracing: bool = Field(default=True, description="Enable distributed tracing")
    zipkin_endpoint: str = Field(default="http://localhost:9411/api/v2/spans", description="Zipkin endpoint")

    # Rate Limiting & Timeouts
    request_timeout: int = Field(default=30, description="HTTP request timeout in seconds")
    max_retries: int = Field(default=3, description="Max retries for failed operations")
    retry_backoff_seconds: int = Field(default=2, description="Retry backoff in seconds")

    # Feature Flags
    enable_streaming_responses: bool = Field(default=False, description="Enable streaming Claude responses")
    enable_websocket: bool = Field(default=True, description="Enable WebSocket for real-time updates")
    enable_caching: bool = Field(default=True, description="Enable response caching")

    @field_validator('log_level')
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level is one of the standard Python logging levels"""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f"log_level must be one of {valid_levels}")
        return v.upper()

    @field_validator('environment')
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment is one of the allowed values"""
        valid_envs = ['development', 'staging', 'production']
        if v.lower() not in valid_envs:
            raise ValueError(f"environment must be one of {valid_envs}")
        return v.lower()

    @property
    def postgres_url(self) -> str:
        """Build PostgreSQL connection URL"""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.environment == "development"


class TriageAgentConfig(AgentConfig):
    """Configuration specific to Triage Agent"""

    agent_name: str = Field(default="triage-agent", description="Agent name")
    agent_port: int = Field(default=8001, description="Agent HTTP port")

    # Triage-specific settings
    max_concurrent_requests: int = Field(default=10, description="Max concurrent query processing")
    routing_confidence_threshold: float = Field(default=0.7, description="Min confidence for routing decision")


class ConceptsAgentConfig(AgentConfig):
    """Configuration specific to Concepts Agent"""

    agent_name: str = Field(default="concepts-agent", description="Agent name")
    agent_port: int = Field(default=8002, description="Agent HTTP port")

    # Concepts-specific settings
    max_example_length: int = Field(default=500, description="Max length for code examples")
    include_visualizations: bool = Field(default=True, description="Include ASCII visualizations")


class CodeReviewAgentConfig(AgentConfig):
    """Configuration specific to Code Review Agent"""

    agent_name: str = Field(default="code-review-agent", description="Agent name")
    agent_port: int = Field(default=8003, description="Agent HTTP port")

    # Code Review-specific settings
    max_code_length: int = Field(default=2000, description="Max code length for review")
    review_depth: str = Field(default="detailed", description="Review depth: quick, detailed, comprehensive")


class DebugAgentConfig(AgentConfig):
    """Configuration specific to Debug Agent"""

    agent_name: str = Field(default="debug-agent", description="Agent name")
    agent_port: int = Field(default=8004, description="Agent HTTP port")

    # Debug-specific settings
    max_stack_trace_lines: int = Field(default=50, description="Max stack trace lines to analyze")
    suggest_fixes: bool = Field(default=True, description="Suggest code fixes")


class ExerciseGeneratorConfig(AgentConfig):
    """Configuration specific to Exercise Generator"""

    agent_name: str = Field(default="exercise-generator-agent", description="Agent name")
    agent_port: int = Field(default=8005, description="Agent HTTP port")

    # Exercise-specific settings
    difficulty_levels: list[str] = Field(default=["beginner", "intermediate", "advanced"], description="Available difficulty levels")
    include_test_cases: bool = Field(default=True, description="Include test cases with exercises")


class ProgressTrackerConfig(AgentConfig):
    """Configuration specific to Progress Tracker"""

    agent_name: str = Field(default="progress-tracker-agent", description="Agent name")
    agent_port: int = Field(default=8006, description="Agent HTTP port")

    # Progress tracking-specific settings
    mastery_threshold: float = Field(default=0.8, description="Mastery threshold (0.0-1.0)")
    update_interval_seconds: int = Field(default=60, description="Progress update interval")


def get_config(agent_type: Optional[str] = None) -> AgentConfig:
    """
    Factory function to get appropriate configuration based on agent type.

    Args:
        agent_type: Type of agent (triage, concepts, code-review, debug, exercise, progress)
                   If None, returns base AgentConfig

    Returns:
        Appropriate configuration instance
    """
    config_map = {
        "triage": TriageAgentConfig,
        "concepts": ConceptsAgentConfig,
        "code-review": CodeReviewAgentConfig,
        "debug": DebugAgentConfig,
        "exercise": ExerciseGeneratorConfig,
        "progress": ProgressTrackerConfig,
    }

    if agent_type is None:
        return AgentConfig()

    config_class = config_map.get(agent_type.lower())
    if config_class is None:
        raise ValueError(f"Unknown agent type: {agent_type}. Valid types: {list(config_map.keys())}")

    return config_class()
