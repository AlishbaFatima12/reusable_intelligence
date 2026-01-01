"""
AGENTS.md markdown generation following AAIF compliance standards.

This module generates AAIF-compliant documentation from extracted agent metadata.
Output is deterministic (sorted) for cross-agent compatibility.
"""
from pathlib import Path
from data_model import AgentMetadata, EndpointMetadata, SchemaMetadata


def generate_markdown(agents: list[AgentMetadata]) -> str:
    """
    Creates AAIF-compliant AGENTS.md with sorted agents/endpoints for deterministic output.

    Args:
        agents: List of AgentMetadata objects

    Returns:
        Complete AGENTS.md content as string

    Examples:
        >>> md = generate_markdown([agent1, agent2])
        >>> "# Agent Architecture" in md
        True
    """
    if not agents:
        return _generate_empty_agents_md()

    # Sort agents by name for deterministic output (cross-agent compatibility)
    sorted_agents = sorted(agents, key=lambda a: a.name)

    sections = []

    # Header
    sections.append(_generate_header(sorted_agents))

    # Each agent section
    for agent in sorted_agents:
        sections.append(_generate_agent_section(agent))

    return "\n\n".join(sections)


def _generate_empty_agents_md() -> str:
    """
    Generates AGENTS.md for projects with no agents discovered.

    Returns:
        Minimal AGENTS.md content
    """
    return """# Agent Architecture

## Overview

No agents detected in this project.

This file is auto-generated. To add agents, create FastAPI applications in the backend/ directory.
"""


def _generate_header(agents: list[AgentMetadata]) -> str:
    """
    Generates the header section with overview.

    Args:
        agents: Sorted list of agents

    Returns:
        Header markdown
    """
    agent_count = len(agents)
    agent_names = ", ".join([agent.name for agent in agents])

    return f"""# Agent Architecture

## Overview

This system consists of {agent_count} microservice agent{"s" if agent_count != 1 else ""}:

{_generate_agent_list(agents)}

Each agent is a FastAPI application with dedicated responsibilities and API contracts."""


def _generate_agent_list(agents: list[AgentMetadata]) -> str:
    """
    Generates bulleted list of agents with ports.

    Args:
        agents: Sorted list of agents

    Returns:
        Markdown bulleted list
    """
    lines = []
    for agent in agents:
        lines.append(f"- **{agent.name}** (port {agent.port}): {agent.purpose}")
    return "\n".join(lines)


def _generate_agent_section(agent: AgentMetadata) -> str:
    """
    Generates complete section for a single agent.

    Args:
        agent: AgentMetadata object

    Returns:
        Agent section markdown
    """
    sections = []

    # Agent header
    sections.append(f"## {agent.name}")
    sections.append("")

    # Basic info
    sections.append(f"**Port**: {agent.port}")
    sections.append(f"**Purpose**: {agent.purpose}")
    sections.append(f"**Location**: `{agent.directory}`")
    sections.append("")

    # Dependencies section
    if agent.dependencies:
        sections.append("### Dependencies")
        sections.append("")
        sections.append(_generate_dependencies_table(agent))
        sections.append("")

    # API Contract section
    if agent.endpoints:
        sections.append("### API Contract")
        sections.append("")
        for endpoint in agent.endpoints:
            sections.append(_generate_endpoint_section(endpoint))
            sections.append("")

    # Pub/Sub section
    sections.append("### Pub/Sub Topics")
    sections.append("")
    sections.append(_generate_pubsub_section(agent))

    return "\n".join(sections)


def _generate_dependencies_table(agent: AgentMetadata) -> str:
    """
    Generates dependencies table.

    Args:
        agent: AgentMetadata object

    Returns:
        Markdown table
    """
    lines = []
    lines.append("| Dependency | Type | Source |")
    lines.append("|------------|------|--------|")

    for dep in agent.dependencies:
        lines.append(f"| {dep.name} | {dep.type_} | {dep.source} |")

    return "\n".join(lines)


def _generate_endpoint_section(endpoint: EndpointMetadata) -> str:
    """
    Generates documentation for a single endpoint.

    Args:
        endpoint: EndpointMetadata object

    Returns:
        Endpoint markdown section
    """
    sections = []

    # Endpoint header
    sections.append(f"#### `{endpoint.method} {endpoint.path}`")
    sections.append("")
    sections.append(endpoint.description)
    sections.append("")

    # Request schema
    if endpoint.request_schema:
        sections.append("**Request**:")
        sections.append("```json")
        sections.append(_generate_schema_example(endpoint.request_schema))
        sections.append("```")
        sections.append("")

    # Response schema
    if endpoint.response_schema:
        sections.append("**Response**:")
        sections.append("```json")
        sections.append(_generate_schema_example(endpoint.response_schema))
        sections.append("```")

    return "\n".join(sections)


def _generate_schema_example(schema: SchemaMetadata) -> str:
    """
    Generates JSON example from Pydantic schema.

    Args:
        schema: SchemaMetadata object

    Returns:
        JSON example string
    """
    if not schema.fields:
        return "{}"

    lines = ["{"]

    for i, field in enumerate(schema.fields):
        # Generate example value based on type
        example_value = _get_example_value(field.type_, field.default)

        # Format as JSON
        comma = "," if i < len(schema.fields) - 1 else ""
        comment = f"  // {field.description}" if field.description else ""

        # Add required/optional indicator
        optional_marker = "" if field.required else " (optional)"

        lines.append(f'  "{field.name}": {example_value}{comma}{optional_marker}{comment}')

    lines.append("}")

    return "\n".join(lines)


def _get_example_value(type_str: str, default: str | None) -> str:
    """
    Generates example value based on type annotation.

    Args:
        type_str: Type annotation string (e.g., "str", "int", "list[str]")
        default: Default value string or None

    Returns:
        JSON-formatted example value
    """
    if default:
        return default

    # Map types to example values
    type_examples = {
        "str": '"string"',
        "int": '0',
        "float": '0.0',
        "bool": 'true',
        "list[str]": '["item1", "item2"]',
        "list[int]": '[1, 2, 3]',
        "dict": '{}',
        "dict[str, str]": '{"key": "value"}',
    }

    # Handle union types (e.g., "dict | None")
    if " | " in type_str:
        base_type = type_str.split(" | ")[0]
        return type_examples.get(base_type, '{}')

    return type_examples.get(type_str, '{}')


def _generate_pubsub_section(agent: AgentMetadata) -> str:
    """
    Generates Pub/Sub topics section.

    Args:
        agent: AgentMetadata object

    Returns:
        Pub/Sub markdown
    """
    sections = []

    if agent.kafka_topics.subscribes:
        sections.append("**Subscribes to**:")
        for topic in agent.kafka_topics.subscribes:
            sections.append(f"- `{topic}`")
        sections.append("")

    if agent.kafka_topics.publishes:
        sections.append("**Publishes to**:")
        for topic in agent.kafka_topics.publishes:
            sections.append(f"- `{topic}`")
        sections.append("")

    if not agent.kafka_topics.subscribes and not agent.kafka_topics.publishes:
        sections.append("No Kafka topics configured.")

    return "\n".join(sections)


def save_agents_md(agents: list[AgentMetadata], output_path: Path) -> None:
    """
    Generates and saves AGENTS.md to file.

    Args:
        agents: List of AgentMetadata objects
        output_path: Path where AGENTS.md should be written
    """
    markdown = generate_markdown(agents)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown)
