# Data Model: AGENTS.md Generator

**Feature**: 001-agents-md-gen
**Date**: 2025-12-29
**Phase**: Phase 1 Design

## Overview

This document defines the internal data structures used by the AGENTS.md documentation generator. These models represent the intermediate metadata extracted from Python codebases before generating markdown output.

## Core Entities

### AgentMetadata

Represents a single microservice agent discovered in the codebase.

**Attributes**:
- `name` (str): Agent name derived from directory (e.g., "triage-agent")
- `port` (int): Network port from config or default (e.g., 8001)
- `purpose` (str): One-sentence description from docstring
- `directory` (Path): Absolute path to agent source directory
- `endpoints` (list[EndpointMetadata]): API endpoints defined in this agent
- `dependencies` (list[DependencyMetadata]): External services required
- `kafka_topics` (KafkaTopics): Pub/sub topic subscriptions and publications

**Validation Rules**:
- `name` must be non-empty string
- `port` must be 1-65535
- `purpose` defaults to "[No description provided]" if missing
- `endpoints` can be empty list (warn if empty)
- `dependencies` can be empty list (valid for standalone agents)

**Example**:
```python
AgentMetadata(
    name="triage-agent",
    port=8001,
    purpose="Routes student queries to appropriate specialist agents via intent classification",
    directory=Path("/backend/triage-agent"),
    endpoints=[...],
    dependencies=[...],
    kafka_topics=KafkaTopics(subscribes=["query.received"], publishes=["query.routed"])
)
```

**State Transitions**: N/A (immutable data structure)

---

### EndpointMetadata

Represents a single API endpoint extracted from FastAPI route decorators.

**Attributes**:
- `method` (str): HTTP method (GET, POST, PUT, DELETE, PATCH)
- `path` (str): URL path pattern (e.g., "/classify", "/items/{item_id}")
- `request_schema` (SchemaMetadata | None): Input Pydantic model
- `response_schema` (SchemaMetadata | None): Output Pydantic model
- `description` (str): Endpoint purpose from docstring
- `is_async` (bool): Whether handler is async def

**Validation Rules**:
- `method` must be in HTTP_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]
- `path` must start with "/"
- `description` defaults to "[No description provided]" if missing
- `request_schema` can be None (valid for GET endpoints with no body)
- `response_schema` can be None (warn if missing)

**Example**:
```python
EndpointMetadata(
    method="POST",
    path="/classify",
    request_schema=SchemaMetadata(name="QueryRequest", fields=[...]),
    response_schema=SchemaMetadata(name="RoutingDecision", fields=[...]),
    description="Classifies query intent and routes to specialist agent",
    is_async=True
)
```

**Relationships**:
- Belongs to one `AgentMetadata` (via `endpoints` list)
- References 0-2 `SchemaMetadata` objects (request and response)

---

### SchemaMetadata

Represents a Pydantic model used for request/response validation.

**Attributes**:
- `name` (str): Model class name (e.g., "QueryRequest")
- `fields` (list[FieldMetadata]): Model fields with types
- `module` (str): Python module where defined (e.g., "models.requests")

**Validation Rules**:
- `name` must be non-empty string
- `fields` must have at least 1 field (empty Pydantic models are invalid)
- `module` can be empty string if unable to determine

**Example**:
```python
SchemaMetadata(
    name="QueryRequest",
    fields=[
        FieldMetadata(name="query", type_="str", required=True, description="Student query text"),
        FieldMetadata(name="student_id", type_="str", required=True, description="Unique student identifier"),
        FieldMetadata(name="context", type_="dict | None", required=False, description="Optional conversation context")
    ],
    module="backend.triage_agent.models"
)
```

**Relationships**:
- Referenced by 0-N `EndpointMetadata` objects (can be shared across endpoints)

---

### FieldMetadata

Represents a single field in a Pydantic model.

**Attributes**:
- `name` (str): Field name (e.g., "query")
- `type_` (str): Python type as string (e.g., "str", "int", "list[str]", "dict | None")
- `required` (bool): Whether field is required (not Optional)
- `description` (str): Field description from Field(description=...) or docstring
- `default` (str | None): Default value as string representation (None if required)

**Validation Rules**:
- `name` must be valid Python identifier
- `type_` must be non-empty string
- `description` defaults to "" if missing
- If `required=False`, `default` should be set (warn if both False and None)

**Example**:
```python
FieldMetadata(
    name="confidence",
    type_="float",
    required=True,
    description="Classification confidence score (0.0-1.0)",
    default=None
)
```

**Relationships**:
- Belongs to one `SchemaMetadata` (via `fields` list)

---

### DependencyMetadata

Represents an external service or package dependency.

**Attributes**:
- `name` (str): Dependency name (e.g., "Claude API", "PostgreSQL", "Kafka")
- `type_` (str): Dependency category (PACKAGE, DATABASE, MESSAGE_QUEUE, API, STORAGE)
- `description` (str): How the agent uses this dependency
- `source` (str): Where detected (IMPORT, ENV_VAR, CONFIG_FILE)

**Validation Rules**:
- `name` must be non-empty string
- `type_` must be in DEPENDENCY_TYPES = ["PACKAGE", "DATABASE", "MESSAGE_QUEUE", "API", "STORAGE", "UNKNOWN"]
- `description` can be empty string
- `source` must be in SOURCES = ["IMPORT", "ENV_VAR", "CONFIG_FILE", "DETECTED"]

**Example**:
```python
DependencyMetadata(
    name="Claude API (Anthropic)",
    type_="API",
    description="Intent classification via Claude Sonnet 4.5",
    source="ENV_VAR"  # Detected from CLAUDE_API_KEY
)
```

**Type Inference Rules**:
```python
def infer_dependency_type(name: str, source: str) -> str:
    """Infer dependency type from name and source."""
    name_lower = name.lower()

    # Database detection
    if any(db in name_lower for db in ["postgres", "mysql", "mongodb", "redis"]):
        return "DATABASE"

    # Message queue detection
    if any(mq in name_lower for mq in ["kafka", "rabbitmq", "redis", "pubsub"]):
        return "MESSAGE_QUEUE"

    # API detection
    if any(api in name_lower for api in ["api", "claude", "openai", "anthropic"]):
        return "API"

    # Package detection (from imports)
    if source == "IMPORT":
        return "PACKAGE"

    return "UNKNOWN"
```

**Relationships**:
- Belongs to one `AgentMetadata` (via `dependencies` list)

---

### KafkaTopics

Represents Kafka pub/sub topic interactions.

**Attributes**:
- `subscribes` (list[str]): Topics this agent subscribes to (consumes from)
- `publishes` (list[str]): Topics this agent publishes to (produces to)

**Validation Rules**:
- Both lists can be empty (valid for non-Kafka agents)
- Topic names should follow convention: lowercase, dot-separated (e.g., "query.received")

**Example**:
```python
KafkaTopics(
    subscribes=["query.received"],
    publishes=["query.routed", "struggle.detected"]
)
```

**Detection Strategy**:
```python
def extract_kafka_topics(agent_dir: Path) -> KafkaTopics:
    """Extract Kafka topics from Dapr pub/sub calls."""
    subscribes = []
    publishes = []

    # Search for patterns:
    # - client.publish_event(pubsub_name="kafka", topic_name="query.routed", ...)
    # - @app.subscribe(pubsub_name="kafka", topic="query.received")

    # Parse AST for function calls and decorators
    # ... (implementation in extract_metadata.py)

    return KafkaTopics(subscribes=subscribes, publishes=publishes)
```

**Relationships**:
- One per `AgentMetadata` (embedded, not separate entity)

---

## Data Flow

### 1. Discovery Phase

```
backend/ directory
    ↓
analyze_agents.py scans subdirectories
    ↓
List[Path] of agent directories
```

### 2. Extraction Phase

```
For each agent directory:
    ↓
extract_metadata.py parses Python files via AST
    ↓
AgentMetadata with:
    - EndpointMetadata list
    - SchemaMetadata list
    - DependencyMetadata list
    - KafkaTopics
```

### 3. Generation Phase

```
List[AgentMetadata]
    ↓
generate_agents_md.py formats as markdown
    ↓
AGENTS.md (AAIF-compliant)
```

### 4. Validation Phase

```
AGENTS.md
    ↓
verify_agents_md.py checks AAIF compliance
    ↓
Validation Report (PASS/FAIL + warnings)
```

## JSON Schema (for serialization)

The metadata structures serialize to JSON for intermediate storage:

```json
{
  "agents": [
    {
      "name": "triage-agent",
      "port": 8001,
      "purpose": "Routes student queries to appropriate specialist agents",
      "directory": "/backend/triage-agent",
      "endpoints": [
        {
          "method": "POST",
          "path": "/classify",
          "request_schema": {
            "name": "QueryRequest",
            "fields": [
              {"name": "query", "type": "str", "required": true, "description": "Student query text"}
            ]
          },
          "response_schema": {...},
          "description": "Classifies query intent",
          "is_async": true
        }
      ],
      "dependencies": [
        {"name": "Claude API", "type": "API", "description": "Intent classification", "source": "ENV_VAR"}
      ],
      "kafka_topics": {
        "subscribes": ["query.received"],
        "publishes": ["query.routed"]
      }
    }
  ]
}
```

This JSON is used for:
- Intermediate storage between scripts (e.g., `analyze_agents.py` → `generate_agents_md.py`)
- Testing fixtures (sample metadata for unit tests)
- Debugging (inspect extracted metadata before markdown generation)

## Type Definitions (Python)

For implementation, use Python dataclasses:

```python
from dataclasses import dataclass
from pathlib import Path

@dataclass
class FieldMetadata:
    name: str
    type_: str
    required: bool
    description: str
    default: str | None = None

@dataclass
class SchemaMetadata:
    name: str
    fields: list[FieldMetadata]
    module: str = ""

@dataclass
class EndpointMetadata:
    method: str
    path: str
    description: str
    request_schema: SchemaMetadata | None = None
    response_schema: SchemaMetadata | None = None
    is_async: bool = True

@dataclass
class DependencyMetadata:
    name: str
    type_: str
    description: str
    source: str

@dataclass
class KafkaTopics:
    subscribes: list[str]
    publishes: list[str]

@dataclass
class AgentMetadata:
    name: str
    port: int
    purpose: str
    directory: Path
    endpoints: list[EndpointMetadata]
    dependencies: list[DependencyMetadata]
    kafka_topics: KafkaTopics
```

## Constraints & Invariants

1. **Agent Uniqueness**: No two agents can have the same `name`
2. **Port Conflicts**: Warn (don't error) if multiple agents use the same port
3. **Schema Consistency**: If an endpoint references a schema, that schema must be fully defined (no incomplete fields)
4. **Kafka Topic Naming**: Topics should match pattern `[a-z]+(\.[a-z]+)*` (lowercase, dot-separated)
5. **Deterministic Ordering**: All lists (agents, endpoints, fields) must be sorted alphabetically for reproducible output

## Next Steps

With data model defined, proceed to:
1. Create `quickstart.md` with skill usage examples
2. Update agent context (if applicable)
3. Ready for `/sp.tasks` to break down implementation
