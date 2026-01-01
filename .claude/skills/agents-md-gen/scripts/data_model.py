"""
Data model for AGENTS.md documentation generator.

This module defines the core data structures used to represent agent metadata
extracted from FastAPI codebases.
"""
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional
import json


@dataclass
class FieldMetadata:
    """Represents a single field in a Pydantic model"""
    name: str
    type_: str  # Python type as string (e.g., "str", "int", "list[str]")
    required: bool
    description: str
    default: Optional[str] = None  # Default value as string representation

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)


@dataclass
class SchemaMetadata:
    """Represents a Pydantic model used for request/response validation"""
    name: str
    fields: list[FieldMetadata]
    module: str = ""  # Python module where defined

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "name": self.name,
            "fields": [f.to_dict() for f in self.fields],
            "module": self.module
        }


@dataclass
class EndpointMetadata:
    """Represents a single API endpoint extracted from FastAPI route decorators"""
    method: str  # GET, POST, PUT, DELETE, PATCH
    path: str  # URL path pattern (e.g., "/classify", "/items/{item_id}")
    description: str
    request_schema: Optional[SchemaMetadata] = None
    response_schema: Optional[SchemaMetadata] = None
    is_async: bool = True

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "method": self.method,
            "path": self.path,
            "description": self.description,
            "request_schema": self.request_schema.to_dict() if self.request_schema else None,
            "response_schema": self.response_schema.to_dict() if self.response_schema else None,
            "is_async": self.is_async
        }


@dataclass
class DependencyMetadata:
    """Represents an external service or package dependency"""
    name: str
    type_: str  # PACKAGE, DATABASE, MESSAGE_QUEUE, API, STORAGE, UNKNOWN
    description: str
    source: str  # IMPORT, ENV_VAR, CONFIG_FILE, DETECTED

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)


@dataclass
class KafkaTopics:
    """Represents Kafka pub/sub topic interactions"""
    subscribes: list[str]  # Topics this agent subscribes to
    publishes: list[str]   # Topics this agent publishes to

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)


@dataclass
class AgentMetadata:
    """Represents a single microservice agent discovered in the codebase"""
    name: str
    port: int
    purpose: str
    directory: str  # Store as string for JSON serialization (convert from Path)
    endpoints: list[EndpointMetadata]
    dependencies: list[DependencyMetadata]
    kafka_topics: KafkaTopics

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "name": self.name,
            "port": self.port,
            "purpose": self.purpose,
            "directory": self.directory,
            "endpoints": [e.to_dict() for e in self.endpoints],
            "dependencies": [d.to_dict() for d in self.dependencies],
            "kafka_topics": self.kafka_topics.to_dict()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'AgentMetadata':
        """Create AgentMetadata from dictionary"""
        return cls(
            name=data["name"],
            port=data["port"],
            purpose=data["purpose"],
            directory=data["directory"],
            endpoints=[
                EndpointMetadata(
                    method=e["method"],
                    path=e["path"],
                    description=e["description"],
                    request_schema=SchemaMetadata(
                        name=e["request_schema"]["name"],
                        fields=[FieldMetadata(**f) for f in e["request_schema"]["fields"]],
                        module=e["request_schema"]["module"]
                    ) if e["request_schema"] else None,
                    response_schema=SchemaMetadata(
                        name=e["response_schema"]["name"],
                        fields=[FieldMetadata(**f) for f in e["response_schema"]["fields"]],
                        module=e["response_schema"]["module"]
                    ) if e["response_schema"] else None,
                    is_async=e["is_async"]
                )
                for e in data["endpoints"]
            ],
            dependencies=[DependencyMetadata(**d) for d in data["dependencies"]],
            kafka_topics=KafkaTopics(**data["kafka_topics"])
        )


def save_metadata(agents: list[AgentMetadata], output_path: Path) -> None:
    """Save agent metadata to JSON file"""
    data = {"agents": [agent.to_dict() for agent in agents]}
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_metadata(input_path: Path) -> list[AgentMetadata]:
    """Load agent metadata from JSON file"""
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [AgentMetadata.from_dict(agent) for agent in data["agents"]]
