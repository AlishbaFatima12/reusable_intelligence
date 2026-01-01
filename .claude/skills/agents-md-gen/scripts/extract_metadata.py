"""
Metadata extraction from FastAPI agent codebases.

This module provides functions to extract agent metadata including:
- Agent name, port, purpose
- API endpoints with request/response schemas
- Pydantic model schemas
- External dependencies
"""
import ast
import os
import re
from pathlib import Path
from typing import Optional
from data_model import (
    EndpointMetadata,
    SchemaMetadata,
    FieldMetadata,
    DependencyMetadata,
    KafkaTopics
)


def extract_agent_name(agent_dir: Path) -> str:
    """
    Derives agent name from directory name.

    Args:
        agent_dir: Path to agent directory

    Returns:
        Agent name (directory name converted to title case)

    Examples:
        >>> extract_agent_name(Path("backend/triage_agent"))
        "Triage Agent"
        >>> extract_agent_name(Path("backend/agent1"))
        "Agent1"
    """
    return agent_dir.name.replace("_", " ").replace("-", " ").title()


def extract_port(agent_dir: Path) -> int:
    """
    Finds port from .env, config files, or defaults to 8000.

    Search order:
    1. .env file (PORT= or <AGENT>_PORT=)
    2. config.py/.yaml/.json files
    3. Default to 8000

    Args:
        agent_dir: Path to agent directory

    Returns:
        Port number (int)

    Examples:
        >>> extract_port(Path("backend/agent1"))
        8000
    """
    # Check .env file
    env_file = agent_dir / ".env"
    if env_file.exists():
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("PORT="):
                        port_str = line.split("=", 1)[1].strip()
                        return int(port_str)
                    # Check for AGENT_NAME_PORT pattern
                    if "_PORT=" in line:
                        port_str = line.split("=", 1)[1].strip()
                        return int(port_str)
        except (ValueError, UnicodeDecodeError):
            pass

    # Check config.py for PORT constant
    config_file = agent_dir / "config.py"
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                source = f.read()
                tree = ast.parse(source)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name) and target.id == "PORT":
                                if isinstance(node.value, ast.Constant):
                                    return int(node.value.value)
        except (SyntaxError, ValueError, UnicodeDecodeError):
            pass

    # Default port
    return 8000


def extract_purpose(agent_dir: Path) -> str:
    """
    Gets purpose from module docstring or defaults to placeholder.

    Args:
        agent_dir: Path to agent directory

    Returns:
        Purpose string (first line of module docstring or default)

    Examples:
        >>> extract_purpose(Path("backend/triage_agent"))
        "Routes student queries to appropriate specialist agents"
    """
    main_file = agent_dir / "main.py"

    if not main_file.exists():
        return "[No description provided]"

    try:
        with open(main_file, 'r', encoding='utf-8') as f:
            source = f.read()

        tree = ast.parse(source)

        # Get module docstring
        docstring = ast.get_docstring(tree)
        if docstring:
            # Return first non-empty line (skip title if multi-line)
            lines = [line.strip() for line in docstring.split('\n') if line.strip()]
            if len(lines) >= 2:
                # Second line is usually the description
                return lines[1]
            elif len(lines) == 1:
                # Single line docstring
                return lines[0]

        return "[No description provided]"

    except (SyntaxError, UnicodeDecodeError):
        return "[No description provided]"


def extract_endpoints(agent_dir: Path) -> list[EndpointMetadata]:
    """
    Parses @app.post/@app.get decorators via AST.

    Args:
        agent_dir: Path to agent directory

    Returns:
        List of EndpointMetadata objects, sorted by path for deterministic output

    Examples:
        >>> endpoints = extract_endpoints(Path("backend/agent1"))
        >>> len(endpoints)
        2
        >>> endpoints[0].method
        'POST'
    """
    main_file = agent_dir / "main.py"

    if not main_file.exists():
        return []

    endpoints = []

    try:
        with open(main_file, 'r', encoding='utf-8') as f:
            source = f.read()

        tree = ast.parse(source)

        # Find all function definitions with FastAPI route decorators
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Check decorators
                for decorator in node.decorator_list:
                    endpoint = _parse_route_decorator(decorator, node)
                    if endpoint:
                        endpoints.append(endpoint)

    except (SyntaxError, UnicodeDecodeError):
        pass

    # Sort by path for deterministic output
    return sorted(endpoints, key=lambda e: e.path)


def _parse_route_decorator(decorator: ast.expr, func_node) -> Optional[EndpointMetadata]:
    """
    Parses a single route decorator to extract endpoint metadata.

    Args:
        decorator: AST decorator node
        func_node: Function definition node

    Returns:
        EndpointMetadata if valid route decorator, None otherwise
    """
    # Pattern: @app.get("/path") or @app.post("/path")
    if not isinstance(decorator, ast.Call):
        return None

    if not isinstance(decorator.func, ast.Attribute):
        return None

    method = decorator.func.attr.upper()
    if method not in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
        return None

    # Extract path from first argument
    if len(decorator.args) == 0:
        return None

    if not isinstance(decorator.args[0], ast.Constant):
        return None

    path = decorator.args[0].value

    # Extract description from function docstring
    description = ast.get_docstring(func_node) or "[No description]"

    # Extract request/response schemas from type hints
    request_schema = None
    response_schema = None

    # Check function signature for request parameter
    if func_node.args.args:
        for arg in func_node.args.args:
            if arg.annotation:
                if isinstance(arg.annotation, ast.Name):
                    # Simple type hint like "request: QueryRequest"
                    request_schema = SchemaMetadata(
                        name=arg.annotation.id,
                        fields=[],  # Will be filled by extract_pydantic_schemas
                        module=""
                    )

    # Check return type annotation
    if func_node.returns:
        if isinstance(func_node.returns, ast.Name):
            response_schema = SchemaMetadata(
                name=func_node.returns.id,
                fields=[],
                module=""
            )

    # Check if function is async
    is_async = isinstance(func_node, ast.AsyncFunctionDef)

    return EndpointMetadata(
        method=method,
        path=path,
        description=description.split('\n')[0],  # First line only
        request_schema=request_schema,
        response_schema=response_schema,
        is_async=is_async
    )


def extract_pydantic_schemas(agent_dir: Path) -> dict[str, SchemaMetadata]:
    """
    Analyzes Pydantic model classes.

    Args:
        agent_dir: Path to agent directory

    Returns:
        Dictionary mapping model name to SchemaMetadata

    Examples:
        >>> schemas = extract_pydantic_schemas(Path("backend/agent1"))
        >>> "QueryRequest" in schemas
        True
    """
    main_file = agent_dir / "main.py"

    if not main_file.exists():
        return {}

    schemas = {}

    try:
        with open(main_file, 'r', encoding='utf-8') as f:
            source = f.read()

        tree = ast.parse(source)

        # Find all class definitions that inherit from BaseModel
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check if inherits from BaseModel
                is_pydantic = False
                for base in node.bases:
                    if isinstance(base, ast.Name) and base.id == "BaseModel":
                        is_pydantic = True
                        break

                if is_pydantic:
                    schema = _parse_pydantic_class(node)
                    schemas[schema.name] = schema

    except (SyntaxError, UnicodeDecodeError):
        pass

    return schemas


def _parse_pydantic_class(class_node: ast.ClassDef) -> SchemaMetadata:
    """
    Parses a Pydantic BaseModel class to extract field metadata.

    Args:
        class_node: AST ClassDef node

    Returns:
        SchemaMetadata with all fields
    """
    fields = []

    for item in class_node.body:
        # Pattern: field_name: field_type = default_value
        if isinstance(item, ast.AnnAssign):
            field = _parse_pydantic_field(item)
            if field:
                fields.append(field)

    # Sort fields alphabetically for deterministic output
    fields.sort(key=lambda f: f.name)

    # Get class docstring for description
    class_doc = ast.get_docstring(class_node) or ""

    return SchemaMetadata(
        name=class_node.name,
        fields=fields,
        module=""  # Will be set later if needed
    )


def _parse_pydantic_field(ann_assign: ast.AnnAssign) -> Optional[FieldMetadata]:
    """
    Parses a single Pydantic field annotation.

    Args:
        ann_assign: AST AnnAssign node

    Returns:
        FieldMetadata or None if invalid
    """
    if not isinstance(ann_assign.target, ast.Name):
        return None

    field_name = ann_assign.target.id

    # Extract type annotation
    type_str = _annotation_to_string(ann_assign.annotation)

    # Check if field is required (no default value)
    required = ann_assign.value is None

    # Extract default value
    default = None
    if ann_assign.value:
        default = _ast_value_to_string(ann_assign.value)

    # Description from inline comment (not easily accessible via AST)
    description = ""

    return FieldMetadata(
        name=field_name,
        type_=type_str,
        required=required,
        description=description,
        default=default
    )


def _annotation_to_string(annotation: ast.expr) -> str:
    """
    Converts AST type annotation to string representation.

    Args:
        annotation: AST annotation node

    Returns:
        Type string (e.g., "str", "list[str]", "dict | None")
    """
    if isinstance(annotation, ast.Name):
        return annotation.id

    if isinstance(annotation, ast.Subscript):
        # Pattern: list[str], dict[str, int]
        base = _annotation_to_string(annotation.value)
        arg = _annotation_to_string(annotation.slice)
        return f"{base}[{arg}]"

    if isinstance(annotation, ast.BinOp):
        # Pattern: dict | None (Python 3.10+ union syntax)
        if isinstance(annotation.op, ast.BitOr):
            left = _annotation_to_string(annotation.left)
            right = _annotation_to_string(annotation.right)
            return f"{left} | {right}"

    if isinstance(annotation, ast.Constant):
        return str(annotation.value)

    if isinstance(annotation, ast.Tuple):
        # Pattern: dict[str, int] where slice is a tuple
        elements = [_annotation_to_string(e) for e in annotation.elts]
        return ", ".join(elements)

    return "Any"


def _ast_value_to_string(value: ast.expr) -> str:
    """
    Converts AST value node to string representation.

    Args:
        value: AST expression node

    Returns:
        String representation of value
    """
    if isinstance(value, ast.Constant):
        if isinstance(value.value, str):
            return f'"{value.value}"'
        return str(value.value)

    if isinstance(value, ast.List):
        return "[]"

    if isinstance(value, ast.Dict):
        return "{}"

    if isinstance(value, ast.Name):
        return value.id

    return "..."


def extract_dependencies(agent_dir: Path) -> list[DependencyMetadata]:
    """
    Analyzes imports and .env variables to identify dependencies.

    Args:
        agent_dir: Path to agent directory

    Returns:
        List of DependencyMetadata, sorted by name for deterministic output

    Examples:
        >>> deps = extract_dependencies(Path("backend/agent1"))
        >>> any(d.name == "fastapi" for d in deps)
        True
    """
    main_file = agent_dir / "main.py"
    dependencies = []

    if not main_file.exists():
        return []

    try:
        with open(main_file, 'r', encoding='utf-8') as f:
            source = f.read()

        tree = ast.parse(source)

        # Extract import dependencies
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    dep = _classify_import_dependency(alias.name)
                    if dep:
                        dependencies.append(dep)

            if isinstance(node, ast.ImportFrom):
                if node.module:
                    dep = _classify_import_dependency(node.module)
                    if dep:
                        dependencies.append(dep)

    except (SyntaxError, UnicodeDecodeError):
        pass

    # Extract .env dependencies
    env_file = agent_dir / ".env"
    if env_file.exists():
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if "=" in line and not line.startswith("#"):
                        key = line.split("=")[0].strip()
                        dep = _classify_env_dependency(key)
                        if dep:
                            dependencies.append(dep)
        except UnicodeDecodeError:
            pass

    # Remove duplicates by name
    seen = set()
    unique_deps = []
    for dep in dependencies:
        if dep.name not in seen:
            seen.add(dep.name)
            unique_deps.append(dep)

    # Sort alphabetically for deterministic output
    return sorted(unique_deps, key=lambda d: d.name)


def _classify_import_dependency(module_name: str) -> Optional[DependencyMetadata]:
    """
    Classifies an imported module as a dependency.

    Args:
        module_name: Name of imported module

    Returns:
        DependencyMetadata or None if should be ignored
    """
    # Ignore standard library and local imports
    stdlib_modules = {
        "ast", "os", "sys", "json", "pathlib", "typing", "dataclasses",
        "datetime", "re", "collections", "itertools", "functools"
    }

    base_module = module_name.split(".")[0]

    if base_module in stdlib_modules:
        return None

    # Classify known packages
    package_types = {
        "fastapi": ("PACKAGE", "FastAPI web framework"),
        "pydantic": ("PACKAGE", "Data validation using Python type hints"),
        "uvicorn": ("PACKAGE", "ASGI server implementation"),
        "sqlalchemy": ("DATABASE", "SQL toolkit and ORM"),
        "psycopg2": ("DATABASE", "PostgreSQL adapter"),
        "pymongo": ("DATABASE", "MongoDB driver"),
        "redis": ("DATABASE", "Redis client"),
        "kafka": ("MESSAGE_QUEUE", "Apache Kafka client"),
        "aiokafka": ("MESSAGE_QUEUE", "Async Kafka client"),
        "celery": ("MESSAGE_QUEUE", "Distributed task queue"),
        "requests": ("API", "HTTP library"),
        "httpx": ("API", "Async HTTP client"),
        "boto3": ("STORAGE", "AWS SDK"),
        "google.cloud": ("STORAGE", "Google Cloud SDK"),
    }

    if base_module in package_types:
        type_, desc = package_types[base_module]
        return DependencyMetadata(
            name=base_module,
            type_=type_,
            description=desc,
            source="IMPORT"
        )

    # Unknown package
    return DependencyMetadata(
        name=base_module,
        type_="PACKAGE",
        description=f"Python package: {module_name}",
        source="IMPORT"
    )


def _classify_env_dependency(env_key: str) -> Optional[DependencyMetadata]:
    """
    Classifies an environment variable as a dependency.

    Args:
        env_key: Environment variable key

    Returns:
        DependencyMetadata or None if should be ignored
    """
    # Ignore common config vars
    ignore_keys = {"PORT", "HOST", "DEBUG", "ENV", "LOG_LEVEL"}

    if env_key in ignore_keys:
        return None

    # Classify by pattern
    if "DATABASE" in env_key or "DB_" in env_key or env_key.endswith("_URL"):
        return DependencyMetadata(
            name=env_key,
            type_="DATABASE",
            description=f"Database connection: {env_key}",
            source="ENV_VAR"
        )

    if "KAFKA" in env_key or "BROKER" in env_key:
        return DependencyMetadata(
            name=env_key,
            type_="MESSAGE_QUEUE",
            description=f"Message queue: {env_key}",
            source="ENV_VAR"
        )

    if "API_KEY" in env_key or "SECRET" in env_key or "TOKEN" in env_key:
        return DependencyMetadata(
            name=env_key,
            type_="API",
            description=f"External API: {env_key}",
            source="ENV_VAR"
        )

    # Unknown env var
    return DependencyMetadata(
        name=env_key,
        type_="UNKNOWN",
        description=f"Environment variable: {env_key}",
        source="ENV_VAR"
    )
