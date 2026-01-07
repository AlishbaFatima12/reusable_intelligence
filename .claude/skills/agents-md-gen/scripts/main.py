"""
Main entry point for AGENTS.md documentation generator.

This script orchestrates the complete workflow:
1. Discover agents in backend directory
2. Extract metadata from each agent
3. Generate AAIF-compliant AGENTS.md
4. Optionally validate output
"""
import sys
import argparse
from pathlib import Path

# Import all modules
from analyze_agents import scan_backend_directory, is_fastapi_agent
from extract_metadata import (
    extract_agent_name,
    extract_port,
    extract_purpose,
    extract_endpoints,
    extract_pydantic_schemas,
    extract_dependencies
)
from data_model import AgentMetadata, KafkaTopics
from generate_agents_md import save_agents_md
from verify_agents_md import validate_and_report


def extract_agent_metadata(agent_dir: Path) -> AgentMetadata:
    """
    Extracts complete metadata for a single agent.

    Args:
        agent_dir: Path to agent directory

    Returns:
        AgentMetadata object with all extracted data
    """
    # Basic metadata
    name = extract_agent_name(agent_dir)
    port = extract_port(agent_dir)
    purpose = extract_purpose(agent_dir)

    # Endpoints
    endpoints = extract_endpoints(agent_dir)

    # Pydantic schemas (for enriching endpoint schemas)
    schemas = extract_pydantic_schemas(agent_dir)

    # Enrich endpoint schemas with field information
    for endpoint in endpoints:
        if endpoint.request_schema and endpoint.request_schema.name in schemas:
            endpoint.request_schema = schemas[endpoint.request_schema.name]
        if endpoint.response_schema and endpoint.response_schema.name in schemas:
            endpoint.response_schema = schemas[endpoint.response_schema.name]

    # Dependencies
    dependencies = extract_dependencies(agent_dir)

    # Kafka topics (placeholder - would need separate detection logic)
    kafka_topics = KafkaTopics(subscribes=[], publishes=[])

    return AgentMetadata(
        name=name,
        port=port,
        purpose=purpose,
        directory=str(agent_dir),
        endpoints=endpoints,
        dependencies=dependencies,
        kafka_topics=kafka_topics
    )


def generate_agents_documentation(backend_path: Path, output_path: Path, validate: bool = False) -> None:
    """
    Complete workflow to generate AGENTS.md.

    Args:
        backend_path: Path to backend directory
        output_path: Path where AGENTS.md should be written
        validate: Whether to run validation after generation
    """
    # Step 1: Discover agent directories
    print(f"Scanning {backend_path} for agents...")
    agent_dirs = scan_backend_directory(backend_path)

    if not agent_dirs:
        print("⚠ No agent directories found")
        print(f"Searched in: {backend_path.absolute()}")
        print("Expected: directories containing main.py files")
        return

    print(f"Found {len(agent_dirs)} potential agent{'s' if len(agent_dirs) != 1 else ''}")

    # Step 2: Filter to FastAPI agents only
    fastapi_agents = []
    for agent_dir in agent_dirs:
        if is_fastapi_agent(agent_dir):
            fastapi_agents.append(agent_dir)
            print(f"  ✓ {agent_dir.name} (FastAPI)")
        else:
            print(f"  ✗ {agent_dir.name} (not FastAPI)")

    if not fastapi_agents:
        print("\n⚠ No FastAPI agents detected")
        print("Agents must contain 'FastAPI()' instantiation in main.py")
        return

    # Step 3: Extract metadata
    print(f"\nExtracting metadata from {len(fastapi_agents)} agent{'s' if len(fastapi_agents) != 1 else ''}...")
    agents_metadata = []

    for agent_dir in fastapi_agents:
        try:
            metadata = extract_agent_metadata(agent_dir)
            agents_metadata.append(metadata)
            print(f"  ✓ {metadata.name}: {len(metadata.endpoints)} endpoint{'s' if len(metadata.endpoints) != 1 else ''}")
        except Exception as e:
            print(f"  ✗ {agent_dir.name}: Error - {e}")

    if not agents_metadata:
        print("\n✗ Failed to extract metadata from any agents")
        return

    # Step 4: Generate AGENTS.md
    print(f"\nGenerating {output_path}...")
    try:
        save_agents_md(agents_metadata, output_path)
        print(f"✓ Generated successfully")
    except Exception as e:
        print(f"✗ Generation failed: {e}")
        return

    # Step 5: Optional validation
    if validate:
        print("\nValidating AGENTS.md...")
        result = validate_and_report(output_path, agents_metadata)
        print(f"Validation: {result}")


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Generate AGENTS.md documentation for FastAPI multi-agent projects"
    )
    parser.add_argument(
        "--backend-dir",
        type=Path,
        default=Path("./backend"),
        help="Path to backend directory containing agent subdirectories (default: ./backend)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("./AGENTS.md"),
        help="Output path for AGENTS.md (default: ./AGENTS.md)"
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Run AAIF compliance validation after generation"
    )

    args = parser.parse_args()

    # Validate inputs
    if not args.backend_dir.exists():
        print(f"✗ Error: Backend directory not found: {args.backend_dir}")
        sys.exit(1)

    if not args.backend_dir.is_dir():
        print(f"✗ Error: Backend path is not a directory: {args.backend_dir}")
        sys.exit(1)

    # Run generation
    try:
        generate_agents_documentation(args.backend_dir, args.output, args.validate)
    except KeyboardInterrupt:
        print("\n\n✗ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
