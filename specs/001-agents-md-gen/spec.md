# Feature Specification: AGENTS.md Documentation Generator

**Feature Branch**: `001-agents-md-gen`
**Created**: 2025-12-29
**Status**: Draft
**Input**: User description: "the constitution created ,see baseline principles of projects and plan"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Auto-Generate Agent Documentation (Priority: P1)

A developer completes building all microservice agents for the LearnFlow platform and wants to generate comprehensive documentation that describes all agents, their responsibilities, and how they interact. They need this documentation to be automatically created from the codebase without manual effort.

**Why this priority**: This is the foundational capability - without automated documentation generation, the skill has no value. This represents the core MVP.

**Independent Test**: Can be fully tested by running the skill on an existing multi-agent codebase and verifying it produces a complete AGENTS.md file that accurately describes all discovered agents. Delivers immediate value by eliminating manual documentation work.

**Acceptance Scenarios**:

1. **Given** a project with 6 microservice agents in the backend/ directory, **When** the documentation generator runs, **Then** it produces an AGENTS.md file listing all 6 agents with their names, ports, and purposes
2. **Given** a FastAPI agent with endpoint definitions, **When** the generator analyzes the agent, **Then** it extracts the agent's API endpoints, request/response schemas, and primary responsibilities
3. **Given** a project with no agents, **When** the generator runs, **Then** it creates an AGENTS.md file indicating no agents were found and provides guidance on expected project structure

---

### User Story 2 - Cross-Agent Compatibility Validation (Priority: P2)

A developer working with multiple AI coding agents (Claude Code, Goose, Aider) wants to ensure the generated documentation works identically across all agents. They need validation that the documentation meets Agent Automation Interoperability Framework (AAIF) standards.

**Why this priority**: Ensures the skill is truly reusable across agent platforms, fulfilling a key constitution principle. Builds on P1 by adding quality validation.

**Independent Test**: Can be tested by running the skill on both Claude Code and Goose, then comparing outputs byte-for-byte. Delivers value by guaranteeing portability.

**Acceptance Scenarios**:

1. **Given** the same codebase analyzed by Claude Code and Goose, **When** both agents run the generator skill, **Then** both produce identical AGENTS.md files
2. **Given** a generated AGENTS.md file, **When** validated against AAIF standards, **Then** all required sections are present (Agent Name, Port, Purpose, Dependencies, API Contract)
3. **Given** an AGENTS.md file from the generator, **When** a developer opens it in any markdown viewer, **Then** all formatting renders correctly with proper headings, tables, and code blocks

---

### User Story 3 - Token Efficiency Reporting (Priority: P3)

A developer wants to understand how efficiently the skill operates compared to traditional manual documentation approaches. They need metrics showing token usage and time savings.

**Why this priority**: Demonstrates the token efficiency principle from the constitution. Nice-to-have validation metric but not essential for core functionality.

**Independent Test**: Can be tested by instrumenting the skill to log token counts and comparing against manual documentation estimates. Delivers value by quantifying efficiency gains.

**Acceptance Scenarios**:

1. **Given** a project with 6 agents, **When** the skill completes, **Then** it reports total tokens used (target: <100 tokens)
2. **Given** token usage data, **When** compared to manual documentation (estimated 5,000+ tokens for reading files and writing docs), **Then** the skill demonstrates 98%+ token reduction
3. **Given** skill execution, **When** validation scripts run, **Then** they return minimal output (~10 tokens) rather than full JSON dumps

---

### Edge Cases

- What happens when an agent directory exists but contains no valid Python/FastAPI code?
- How does the system handle agents with non-standard port configurations or missing port definitions?
- What occurs when two agents claim the same port number?
- How does the generator behave when API endpoint decorators use complex routing patterns or dynamic paths?
- What happens when an agent has dependencies on external services not present in the codebase?
- How does the system handle incomplete docstrings or missing type hints in agent code?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST scan the backend/ directory recursively to discover all microservice agents
- **FR-002**: System MUST identify agents by detecting FastAPI application instances (app = FastAPI())
- **FR-003**: System MUST extract agent metadata including name (from directory), port (from config or defaults), and purpose (from docstrings)
- **FR-004**: System MUST parse FastAPI route decorators (@app.post, @app.get, etc.) to document API endpoints
- **FR-005**: System MUST extract request and response schemas from Pydantic models referenced in endpoint signatures
- **FR-006**: System MUST identify agent dependencies by analyzing import statements and environment variables
- **FR-007**: System MUST generate AGENTS.md in markdown format with standardized sections for each agent
- **FR-008**: System MUST include a system architecture diagram showing agent interactions via Kafka topics
- **FR-009**: System MUST validate generated documentation against AAIF compliance checklist
- **FR-010**: System MUST produce identical output when run by different AI agents (Claude Code, Goose) on the same codebase
- **FR-011**: System MUST complete documentation generation in a single prompt execution without manual intervention
- **FR-012**: System MUST report token usage metrics for the generation process
- **FR-013**: System MUST handle projects with zero agents gracefully by creating an instructional AGENTS.md
- **FR-014**: System MUST detect and report conflicts (duplicate ports, missing dependencies)
- **FR-015**: System MUST preserve existing AGENTS.md sections marked with <!-- PRESERVE --> tags if file already exists

### Key Entities

- **Agent**: A microservice application with a name, port, purpose, API endpoints, dependencies, and Kafka topic subscriptions/publications
- **API Endpoint**: A route definition with HTTP method, path, request schema, response schema, and description
- **Dependency**: An external service, database, or message queue required by an agent (e.g., PostgreSQL, Kafka, Claude API)
- **Kafka Topic**: A message channel that agents publish to or subscribe from (e.g., query.received, response.ready)
- **AGENTS.md**: A markdown documentation file containing all discovered agents organized by name, with architecture diagrams and interaction patterns

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Developers can generate complete AGENTS.md documentation for a 6-agent system in under 30 seconds
- **SC-002**: Generated documentation uses less than 100 tokens during the generation process (98%+ reduction vs manual)
- **SC-003**: Documentation is identical when generated by Claude Code and Goose (byte-for-byte comparison passes)
- **SC-004**: 100% of discovered agents are accurately documented with all required fields (name, port, purpose, endpoints)
- **SC-005**: 95% of API endpoints are correctly extracted with accurate request/response schemas
- **SC-006**: Zero manual edits required for generated documentation to be production-ready
- **SC-007**: Documentation validation passes AAIF compliance checks on first run
- **SC-008**: Developers save 2+ hours per project by using automated generation instead of manual documentation
- **SC-009**: System correctly handles edge cases (0 agents, duplicate ports, missing deps) without crashing
- **SC-010**: Generated AGENTS.md file renders correctly in GitHub, GitLab, VS Code, and other common markdown viewers

## Assumptions

- All microservice agents follow FastAPI framework conventions
- Agents are organized in subdirectories under backend/ (e.g., backend/triage-agent/, backend/concepts-agent/)
- Port configurations are defined in environment variables, config files, or use standard defaults (8001-8006)
- API endpoint docstrings follow standard Python conventions (triple-quoted strings under route decorator)
- Pydantic models are used for request/response validation
- Kafka topic names follow the existing naming convention (e.g., query.received, query.routed, response.ready)
- The skill will be implemented as a Claude Code/Goose-compatible skill with SKILL.md and executable scripts
- Token measurement uses standard token counting methods (approximate word count * 1.3 for English text)

## Out of Scope

- Generating documentation for non-Python microservices (Node.js, Go, etc.)
- Auto-updating AGENTS.md on every code change (CI/CD integration)
- Generating API client libraries or SDKs from the documentation
- Creating interactive API documentation (like Swagger/OpenAPI UIs)
- Analyzing runtime behavior or performance metrics of agents
- Generating deployment manifests or Kubernetes configurations
- Translating documentation into multiple languages
- Versioning documentation across different releases
