"""
AAIF compliance validation for generated AGENTS.md files.

This module validates that generated documentation meets AAIF standards
and identifies potential issues like port conflicts.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from data_model import AgentMetadata


@dataclass
class ValidationReport:
    """Results of AAIF compliance validation"""
    passed: bool
    warnings: list[str]
    errors: list[str]
    missing_sections: list[str]

    def has_issues(self) -> bool:
        """Check if report has any warnings or errors"""
        return bool(self.warnings or self.errors or self.missing_sections)


def validate_aaif_compliance(md_path: Path) -> ValidationReport:
    """
    Checks for required sections (Agent Name, Port, Purpose, Dependencies, API Contract, Pub/Sub).

    Args:
        md_path: Path to AGENTS.md file to validate

    Returns:
        ValidationReport with compliance status

    Examples:
        >>> report = validate_aaif_compliance(Path("AGENTS.md"))
        >>> report.passed
        True
    """
    if not md_path.exists():
        return ValidationReport(
            passed=False,
            warnings=[],
            errors=["AGENTS.md file not found"],
            missing_sections=[]
        )

    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return ValidationReport(
            passed=False,
            warnings=[],
            errors=["AGENTS.md has invalid UTF-8 encoding"],
            missing_sections=[]
        )

    # Required AAIF sections
    required_sections = [
        "# Agent Architecture",
        "## Overview",
        "**Port**:",
        "**Purpose**:",
        "### Dependencies",
        "### API Contract",
        "### Pub/Sub Topics"
    ]

    missing_sections = []
    warnings = []
    errors = []

    # Check for required sections
    for section in required_sections:
        if section not in content:
            # Special case: if no agents, some sections won't exist
            if "No agents detected" in content:
                continue
            missing_sections.append(section)

    # Check for common formatting issues
    if "## " in content:
        # Count agent sections (should be > 0)
        agent_count = content.count("**Port**:")
        if agent_count == 0 and "No agents detected" not in content:
            warnings.append("No agents documented (found header but no agent sections)")

    # Check markdown validity
    if not content.startswith("# "):
        errors.append("File should start with H1 header")

    # Check for empty dependencies/endpoints sections
    if "### Dependencies" in content:
        # Check if followed by actual content
        if "### Dependencies\n\n### " in content.replace("\r\n", "\n"):
            warnings.append("Empty Dependencies section detected")

    # Determine pass/fail
    passed = len(errors) == 0 and len(missing_sections) == 0

    return ValidationReport(
        passed=passed,
        warnings=warnings,
        errors=errors,
        missing_sections=missing_sections
    )


def check_port_conflicts(agents: list[AgentMetadata]) -> list[str]:
    """
    Detects duplicate port numbers.

    Args:
        agents: List of AgentMetadata objects

    Returns:
        List of warning messages about port conflicts

    Examples:
        >>> warnings = check_port_conflicts([agent1, agent2])
        >>> len(warnings)
        0
    """
    port_map: dict[int, list[str]] = {}

    # Group agents by port
    for agent in agents:
        if agent.port not in port_map:
            port_map[agent.port] = []
        port_map[agent.port].append(agent.name)

    # Find conflicts
    conflicts = []
    for port, agent_names in port_map.items():
        if len(agent_names) > 1:
            agents_str = ", ".join(agent_names)
            conflicts.append(f"Port {port} conflict: {agents_str}")

    return conflicts


def format_validation_output(report: ValidationReport) -> str:
    """
    Returns concise summary (<10 tokens: "✓ PASS" or "✗ FAIL: 2 warnings").

    Args:
        report: ValidationReport object

    Returns:
        Concise validation summary

    Examples:
        >>> output = format_validation_output(report)
        >>> "✓ PASS" in output or "✗ FAIL" in output
        True
    """
    if report.passed and not report.has_issues():
        return "✓ PASS"

    # Count issues
    issue_count = len(report.errors) + len(report.warnings) + len(report.missing_sections)

    if report.errors or report.missing_sections:
        return f"✗ FAIL: {issue_count} issue{'s' if issue_count != 1 else ''}"

    # Only warnings
    return f"⚠ PASS: {issue_count} warning{'s' if issue_count != 1 else ''}"


def validate_and_report(md_path: Path, agents: list[AgentMetadata]) -> str:
    """
    Complete validation workflow with formatted output.

    Args:
        md_path: Path to AGENTS.md
        agents: List of AgentMetadata objects

    Returns:
        Formatted validation report (<10 tokens)
    """
    # AAIF compliance check
    report = validate_aaif_compliance(md_path)

    # Port conflict check
    port_warnings = check_port_conflicts(agents)

    # Add port conflicts to report
    if port_warnings:
        report.warnings.extend(port_warnings)
        report.passed = False  # Port conflicts are failures

    return format_validation_output(report)
