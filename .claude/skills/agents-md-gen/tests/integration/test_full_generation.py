"""
End-to-end integration test for AGENTS.md generation.

This test runs all scripts on sample_backend/ and validates AGENTS.md output.
"""
import sys
from pathlib import Path

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

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
from generate_agents_md import generate_markdown, save_agents_md
from verify_agents_md import validate_aaif_compliance, check_port_conflicts


def test_full_generation():
    """
    Integration test: Generate AGENTS.md from sample_backend/ and validate.

    Test steps:
    1. Discover agents in fixtures/sample_backend/
    2. Extract metadata
    3. Generate AGENTS.md
    4. Validate AAIF compliance
    5. Check for port conflicts
    """
    # Setup paths
    fixtures_dir = Path(__file__).parent / "fixtures"
    backend_path = fixtures_dir / "sample_backend"
    output_path = fixtures_dir / "AGENTS_TEST.md"

    print("=" * 60)
    print("INTEGRATION TEST: Full AGENTS.md Generation")
    print("=" * 60)

    # Test 1: Agent Discovery
    print("\n[1/5] Testing agent discovery...")
    agent_dirs = scan_backend_directory(backend_path)
    assert len(agent_dirs) > 0, "Should discover at least one agent directory"
    print(f"  [OK] Found {len(agent_dirs)} agent directory(ies)")

    # Test 2: FastAPI Detection
    print("\n[2/5] Testing FastAPI detection...")
    fastapi_agents = [d for d in agent_dirs if is_fastapi_agent(d)]
    assert len(fastapi_agents) == 2, f"Expected 2 FastAPI agents, found {len(fastapi_agents)}"
    print(f"  [OK] Detected {len(fastapi_agents)} FastAPI agents")

    # Test 3: Metadata Extraction
    print("\n[3/5] Testing metadata extraction...")
    agents_metadata = []

    for agent_dir in fastapi_agents:
        # Extract all metadata
        name = extract_agent_name(agent_dir)
        port = extract_port(agent_dir)
        purpose = extract_purpose(agent_dir)
        endpoints = extract_endpoints(agent_dir)
        schemas = extract_pydantic_schemas(agent_dir)
        dependencies = extract_dependencies(agent_dir)

        # Enrich endpoints with schema details
        for endpoint in endpoints:
            if endpoint.request_schema and endpoint.request_schema.name in schemas:
                endpoint.request_schema = schemas[endpoint.request_schema.name]
            if endpoint.response_schema and endpoint.response_schema.name in schemas:
                endpoint.response_schema = schemas[endpoint.response_schema.name]

        # Create AgentMetadata
        metadata = AgentMetadata(
            name=name,
            port=port,
            purpose=purpose,
            directory=str(agent_dir),
            endpoints=endpoints,
            dependencies=dependencies,
            kafka_topics=KafkaTopics(subscribes=[], publishes=[])
        )

        agents_metadata.append(metadata)
        print(f"  [OK] {name}: {len(endpoints)} endpoints, {len(dependencies)} dependencies")

    assert len(agents_metadata) == 2, "Should extract metadata for 2 agents"

    # Test 4: AGENTS.md Generation
    print("\n[4/5] Testing AGENTS.md generation...")
    markdown = generate_markdown(agents_metadata)
    assert "# Agent Architecture" in markdown, "Should contain header"
    assert "## Agent1" in markdown or "## Triage" in markdown, "Should contain agent sections"
    assert "### API Contract" in markdown, "Should contain API contract sections"

    # Save to file
    save_agents_md(agents_metadata, output_path)
    assert output_path.exists(), "Should create AGENTS.md file"
    print(f"  [OK] Generated {output_path}")

    # Test 5: Validation
    print("\n[5/5] Testing AAIF validation...")
    report = validate_aaif_compliance(output_path)

    if not report.passed:
        print(f"  [FAIL] Validation failed:")
        for error in report.errors:
            print(f"    - ERROR: {error}")
        for missing in report.missing_sections:
            print(f"    - MISSING: {missing}")
        for warning in report.warnings:
            print(f"    - WARNING: {warning}")
        assert False, "AAIF validation failed"

    # Check port conflicts
    port_warnings = check_port_conflicts(agents_metadata)
    if port_warnings:
        print(f"  [WARN] Port conflicts detected:")
        for warning in port_warnings:
            print(f"    - {warning}")

    print(f"  [OK] AAIF validation passed")

    # Cleanup
    if output_path.exists():
        output_path.unlink()

    print("\n" + "=" * 60)
    print("[SUCCESS] ALL TESTS PASSED")
    print("=" * 60)


def test_empty_directory():
    """
    Test edge case: empty directory with no agents.
    """
    print("\n" + "=" * 60)
    print("EDGE CASE TEST: Empty Directory")
    print("=" * 60)

    # Create temporary empty directory
    fixtures_dir = Path(__file__).parent / "fixtures"
    empty_dir = fixtures_dir / "empty_backend"
    empty_dir.mkdir(exist_ok=True)

    # Test discovery
    agent_dirs = scan_backend_directory(empty_dir)
    assert len(agent_dirs) == 0, "Should find no agents in empty directory"
    print("  [OK] Empty directory handled correctly")

    # Test markdown generation with empty list
    markdown = generate_markdown([])
    assert "No agents detected" in markdown, "Should handle empty agent list"
    print("  [OK] Empty agent list handled correctly")

    # Cleanup
    if empty_dir.exists():
        empty_dir.rmdir()

    print("=" * 60)
    print("[SUCCESS] EDGE CASE TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    try:
        test_full_generation()
        test_empty_directory()
        print("\n[SUCCESS] All integration tests passed!")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[FAIL] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
