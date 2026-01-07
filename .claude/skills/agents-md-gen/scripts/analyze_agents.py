"""
Agent discovery and analysis for FastAPI microservices.

This module provides functions to:
1. Scan backend directories for potential agent directories
2. Identify FastAPI applications via AST parsing
"""
import ast
from pathlib import Path


def scan_backend_directory(backend_path: Path) -> list[Path]:
    """
    Recursively discovers agent directories containing main.py files.

    Args:
        backend_path: Root directory to scan (e.g., "backend/")

    Returns:
        List of directory paths containing main.py files, sorted alphabetically
        for deterministic output across agents.

    Examples:
        >>> scan_backend_directory(Path("backend"))
        [Path("backend/agent1"), Path("backend/agent2")]
    """
    if not backend_path.exists():
        return []

    if not backend_path.is_dir():
        return []

    agent_dirs = []

    # Recursively find all main.py files
    for main_file in backend_path.rglob("main.py"):
        agent_dir = main_file.parent
        agent_dirs.append(agent_dir)

    # Sort alphabetically for deterministic output (cross-agent compatibility)
    return sorted(agent_dirs)


def is_fastapi_agent(agent_dir: Path) -> bool:
    """
    Detects FastAPI() instances via AST parsing.

    Args:
        agent_dir: Directory containing main.py to analyze

    Returns:
        True if main.py contains FastAPI() instantiation, False otherwise.

    Examples:
        >>> is_fastapi_agent(Path("backend/agent1"))
        True
        >>> is_fastapi_agent(Path("backend/non_fastapi_service"))
        False
    """
    main_file = agent_dir / "main.py"

    if not main_file.exists():
        return False

    try:
        with open(main_file, 'r', encoding='utf-8') as f:
            source = f.read()

        tree = ast.parse(source)

        # Look for FastAPI() instantiation patterns
        for node in ast.walk(tree):
            # Pattern 1: app = FastAPI()
            if isinstance(node, ast.Assign):
                if isinstance(node.value, ast.Call):
                    if isinstance(node.value.func, ast.Name):
                        if node.value.func.id == "FastAPI":
                            return True

            # Pattern 2: FastAPI() in expressions
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id == "FastAPI":
                        return True

        return False

    except (SyntaxError, UnicodeDecodeError):
        # Invalid Python file or encoding issues
        return False
