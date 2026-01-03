# Implementation Plan: LearnFlow Multi-Agent Learning Platform

**Branch**: `002-learnflow-platform` | **Date**: 2026-01-02 | **Spec**: [specs/002-learnflow-platform/spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-learnflow-platform/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

**Primary Requirement**: Build a visual multi-agent learning platform where 6 specialist AI agents (Triage, Concepts, Code Review, Debug, Exercise Generator, Progress Tracker) collaborate to provide personalized programming education. Students submit questions via chat interface, system routes queries to appropriate specialist agents, and responses are delivered with full transparency of the agent workflow.

**Technical Approach**:
- Event-driven microservices architecture with 6 FastAPI backend agents communicating via Kafka pub/sub
- Dapr sidecars for state management (PostgreSQL), service invocation, and secrets handling
- Claude API integration at runtime for AI-powered agent responses (not build-time)
- Real-time frontend updates via WebSocket for agent status and message flow visualization
- Integration with existing Mystery Skills UI (Next.js 15 + Three.js + React 19) for 3D visualization dashboard

## Technical Context

**Language/Version**: Python 3.11+ (backend agents), TypeScript 5.3+ (frontend)

**Primary Dependencies**:
  - Backend: FastAPI 0.109+, Dapr SDK 1.13+, Anthropic SDK 0.18+, Kafka-python 2.0+, Pydantic 2.0+
  - Frontend: Next.js 15, React 19, Three.js, Socket.io-client, Framer Motion

**Storage**: PostgreSQL 15+ via Dapr state store component (state.postgresql)

**Testing**:
  - Backend: pytest, pytest-asyncio, httpx (async client testing)
  - Frontend: Jest, React Testing Library
  - Integration: pytest with Kafka/Dapr testcontainers
  - Contract: Pact or custom JSON schema validation

**Target Platform**:
  - Backend: Kubernetes (Minikube for local dev, cloud for production)
  - Frontend: Vercel or Kubernetes with Next.js standalone build
  - Development: Docker Compose for local orchestration

**Project Type**: Web application (microservices backend + Next.js frontend)

**Performance Goals**:
  - Simple queries (concept explanations): <5s end-to-end response time
  - Complex queries (code review, debugging): <15s end-to-end response time
  - Triage routing decision: <2s p95 latency
  - Dashboard real-time updates: <1s latency from agent state change
  - Concurrent query handling: 100+ simultaneous student queries without degradation

**Constraints**:
  - API latency: <500ms p95 for query routing (Triage Agent)
  - Database queries: Optimized with indexes, connection pooling
  - Frontend bundle: <500KB initial load (code-split by route)
  - Claude API rate limits: 100 req/sec per agent (implement exponential backoff)
  - Student query timeout: 30s (after which graceful error shown)
  - Real-time updates: <1s from agent event to UI update

**Scale/Scope**:
  - Target users: 10,000 concurrent students
  - Query volume: 1,000 queries/min peak load
  - Data retention: 90 days query history, indefinite progress tracking
  - Agent uptime: 99.9% SLA
  - Frontend: 6 core components (3D Sphere, Terminal, HUD, Chat, Agent Cards, Message Flow)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Agent-Native Development ✅ PASS

**Evaluation**: This feature exemplifies agent-native development. AI agents are the **product runtime**, not just build tools.

- **Agents as Digital FTEs**: Each of the 6 specialist agents (Triage, Concepts, Code Review, Debug, Exercise, Progress) operates autonomously using Claude API at runtime
- **Specs as Executable Blueprints**: Feature spec defines intent, success criteria, and behavior; agents make routing and response decisions independently
- **Build + Runtime Autonomy**: Agents build the system (via SDD workflow) AND operate it (via Claude API at runtime for student queries)
- **Skills Composable**: Can leverage existing `agents-md-gen` skill for documentation; future skills for deployment/monitoring

**Justification**: LearnFlow is the gold standard for AI-native runtime per Constitution Section VI.

---

### II. Token Efficiency ✅ PASS (with monitoring)

**Evaluation**: Design follows MCP Code Execution Pattern; requires active monitoring during implementation.

- **Scripts Execute Externally**: Dapr/Kafka deployment via executable bash scripts (0 tokens in context)
- **Validation Output**: Health checks return minimal JSON summaries (~10 tokens: `{"status": "healthy", "agents": 6}`)
- **No Raw Data Dumps**: Agent logs streamed via Kafka to frontend; not loaded into agent context
- **Skills On-Demand**: Documentation skill loaded only when needed (~100 tokens)

**Risks**:
- Claude API responses at runtime consume tokens (but necessary for product functionality)
- Large query histories could bloat context if not properly paginated

**Mitigation**:
- Implement pagination for query history (max 50 queries per API call)
- Use Dapr state store for persistence; only load minimal context into Claude prompts
- Monitor token usage during development; target <1000 tokens for full deployment

---

### III. Spec-Driven Development ✅ PASS

**Evaluation**: Feature follows SDD mandate strictly.

- **Specification First**: Feature spec (`spec.md`) completed before any implementation
- **Version Controlled**: Spec tracked in Git at `specs/002-learnflow-platform/`
- **Autonomous Decisions**: Agents use spec to determine routing logic, error handling, response formats
- **No Code Without Spec**: This plan blocks Phase 0 research until constitution check passes

**Evidence**: Current workflow demonstrates SDD compliance (spec → plan → research → data-model → tasks → implementation).

---

### IV. Event-Driven Cloud-Native Architecture ✅ PASS

**Evaluation**: Architecture is textbook cloud-native per Constitution Section V.

**Microservices**:
- 6 independent FastAPI services (1 per agent)
- Each agent runs on separate port (8001-8006)
- Stateless compute (all state in PostgreSQL via Dapr)

**Pub/Sub Communication**:
- Kafka topics for inter-agent messaging (`student-queries`, `agent-responses`, `agent-logs`, `student-struggle`)
- Loose coupling via event-driven routing
- Dapr pub/sub component abstracts Kafka complexity

**State Management**:
- PostgreSQL via Dapr state store component
- Connection pooling, read replicas for scale
- Agent-specific state keys (e.g., `progress-tracker:student123`)

**Kubernetes Deployment**:
- Each agent deployable independently
- Horizontal scaling via Kubernetes HPA (based on Kafka consumer lag)
- Health checks (liveness/readiness probes)

**Observability**:
- Structured JSON logging (timestamp, level, service, message, trace_id)
- Prometheus metrics (request count, latency, error rate)
- Distributed tracing via Dapr (Jaeger/Zipkin)

**Compliance**: Fully aligned with Constitution technical stack (FastAPI + Dapr + Kafka + PostgreSQL + Kubernetes).

---

### V. AI-Native Runtime ✅ PASS

**Evaluation**: This is the **LearnFlow Gold Standard** referenced in Constitution Section VI.

**Runtime LLM Integration**:
- All 6 agents use Claude API at runtime for query processing (not build-time code generation)
- Concepts Agent: Generates explanations with code examples dynamically
- Code Review Agent: Analyzes submitted code in real-time
- Debug Agent: Identifies errors and suggests fixes on-demand
- Exercise Generator: Creates personalized practice problems
- Progress Tracker: Provides AI-generated learning insights

**Agent Collaboration**:
- Triage Agent routes queries to specialists via Kafka pub/sub
- Multi-agent workflows (e.g., Debug → Concepts) coordinated via events
- Message flow tracked end-to-end for transparency

**Self-Healing**:
- Kubernetes liveness/readiness probes restart unhealthy agents
- Dapr retry policies for transient Kafka failures
- Circuit breaker pattern for Claude API rate limit handling

**Learning from Interactions**:
- Progress Tracker stores successful explanations in PostgreSQL
- Future enhancement: Vector database for semantic search of past responses

**Compliance**: Exceeds constitution requirements; sets benchmark for AI-native architecture.

---

### VI. Testing & Validation ✅ PASS

**Evaluation**: Comprehensive testing strategy defined.

**Test Types**:
- **Unit Tests**: Business logic for routing, response generation (pytest)
- **Integration Tests**: Kafka pub/sub, Dapr state management (testcontainers)
- **Contract Tests**: API endpoints, message schemas (Pact or JSON schema validation)
- **End-to-End Tests**: User flows (student submits query → receives response)

**Automation**:
- CI pipeline runs tests before deployment (GitHub Actions)
- Validation scripts check agent health before marking deployment successful
- Tests block deployment on failure (no manual overrides)

**Validation Scripts**:
- `verify-agents.py`: Returns `{"status": "healthy", "agents": 6, "uptime": "99.9%"}` (~10 tokens)
- `verify-kafka.py`: Returns `{"topics": 4, "partitions": 12, "lag": "0"}` (~10 tokens)

**Compliance**: Meets constitution requirement for autonomous validation with minimal output.

---

### VII. Documentation as Code ✅ PASS

**Evaluation**: Documentation auto-generated and version-controlled.

**Auto-Generated Docs**:
- `AGENTS.md`: Generated via `agents-md-gen` skill (AST-based extraction from FastAPI code)
- API docs: Swagger/OpenAPI via FastAPI (auto-deployed to Docusaurus)
- Architecture diagrams: Embedded in specs (Mermaid or PlantUML)

**ADR Process**:
- Architectural decisions documented after planning phase
- Example ADRs: "Why Kafka over RabbitMQ?", "Why separate agent per microservice vs monolith?"
- ADRs stored at `history/adr/` with title, context, decision, consequences

**Compliance**: Aligns with constitution requirement for doc-as-code and prompted ADRs.

---

### Constitution Check Summary

| Principle | Status | Notes |
|-----------|--------|-------|
| Agent-Native Development | ✅ PASS | Agents are runtime product components |
| Token Efficiency | ✅ PASS | Requires monitoring; scripts execute externally |
| Spec-Driven Development | ✅ PASS | Spec-first workflow enforced |
| Event-Driven Architecture | ✅ PASS | Textbook cloud-native design |
| AI-Native Runtime | ✅ PASS | Gold standard for LLM integration |
| Testing & Validation | ✅ PASS | Autonomous validation with minimal output |
| Documentation as Code | ✅ PASS | Auto-generated from code and specs |

**GATE RESULT**: ✅ **APPROVED** - Proceed to Phase 0 research.

## Project Structure

### Documentation (this feature)

```text
specs/002-learnflow-platform/
├── spec.md              # Feature specification (COMPLETE)
├── plan.md              # This file (COMPLETE)
├── research.md          # Phase 0 output (TODO - /sp.plan command)
├── data-model.md        # Phase 1 output (TODO - /sp.plan command)
├── quickstart.md        # Phase 1 output (TODO - /sp.plan command)
├── contracts/           # Phase 1 output (TODO - /sp.plan command)
│   ├── triage-api.yaml          # OpenAPI spec for Triage Agent (port 8001)
│   ├── concepts-api.yaml        # OpenAPI spec for Concepts Agent (port 8002)
│   ├── code-review-api.yaml     # OpenAPI spec for Code Review Agent (port 8003)
│   ├── debug-api.yaml           # OpenAPI spec for Debug Agent (port 8004)
│   ├── exercise-api.yaml        # OpenAPI spec for Exercise Generator (port 8005)
│   ├── progress-api.yaml        # OpenAPI spec for Progress Tracker (port 8006)
│   ├── kafka-topics.yaml        # Kafka topic schemas (student-queries, agent-responses, etc.)
│   └── dapr-components.yaml     # Dapr component configurations
└── tasks.md             # Phase 2 output (TODO - /sp.tasks command)
```

### Source Code (repository root)

```text
# Backend: 6 FastAPI microservices
backend/
├── agents/
│   ├── triage/                   # Port 8001 - Query routing
│   │   ├── main.py               # FastAPI app entry point
│   │   ├── routes.py             # /analyze, /route endpoints
│   │   ├── models.py             # Pydantic models (Query, RoutingDecision)
│   │   ├── services/
│   │   │   ├── classifier.py    # Intent classification logic (uses Claude API)
│   │   │   ├── kafka_producer.py # Publish to agent topics
│   │   │   └── dapr_client.py   # Dapr service invocation
│   │   ├── config.py             # Environment variables, Anthropic API key
│   │   ├── Dockerfile            # Multi-stage build for production
│   │   └── requirements.txt      # FastAPI, dapr-sdk, anthropic, kafka-python
│   │
│   ├── concepts/                 # Port 8002 - Programming concept explanations
│   │   ├── main.py
│   │   ├── routes.py             # /explain endpoint
│   │   ├── models.py             # Pydantic models (ConceptQuery, Explanation)
│   │   ├── services/
│   │   │   ├── explainer.py     # Claude API for generating explanations
│   │   │   ├── kafka_consumer.py # Subscribe to concepts-queries topic
│   │   │   └── state_manager.py # Dapr state store for caching explanations
│   │   ├── config.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── code-review/              # Port 8003 - Code quality feedback
│   │   ├── main.py
│   │   ├── routes.py             # /review endpoint
│   │   ├── models.py             # Pydantic models (CodeSubmission, ReviewFeedback)
│   │   ├── services/
│   │   │   ├── reviewer.py      # Claude API for code analysis
│   │   │   ├── kafka_consumer.py
│   │   │   └── linter_integration.py # Optional: Flake8, ESLint integration
│   │   ├── config.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── debug/                    # Port 8004 - Error diagnosis
│   │   ├── main.py
│   │   ├── routes.py             # /diagnose endpoint
│   │   ├── models.py             # Pydantic models (DebugRequest, DiagnosisResult)
│   │   ├── services/
│   │   │   ├── debugger.py      # Claude API for error analysis
│   │   │   ├── kafka_consumer.py
│   │   │   └── error_parser.py  # Parse stack traces, syntax errors
│   │   ├── config.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── exercise/                 # Port 8005 - Practice problem generation
│   │   ├── main.py
│   │   ├── routes.py             # /generate endpoint
│   │   ├── models.py             # Pydantic models (ExerciseRequest, GeneratedExercise)
│   │   ├── services/
│   │   │   ├── generator.py     # Claude API for creating exercises
│   │   │   ├── kafka_consumer.py
│   │   │   └── difficulty_scaler.py # Adjust problem difficulty
│   │   ├── config.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   └── progress/                 # Port 8006 - Learning analytics
│       ├── main.py
│       ├── routes.py             # /mastery, /insights endpoints
│       ├── models.py             # Pydantic models (ProgressUpdate, MasteryReport)
│       ├── services/
│       │   ├── tracker.py       # Track student milestones, topics
│       │   ├── analytics.py     # Generate learning insights (uses Claude API)
│       │   ├── kafka_consumer.py # Subscribe to all agent responses
│       │   └── state_manager.py # Dapr state store for student progress
│       ├── config.py
│       ├── Dockerfile
│       └── requirements.txt
│
├── shared/                       # Shared utilities across agents
│   ├── logging_config.py         # Structured JSON logging setup
│   ├── health_checks.py          # /health, /ready endpoint handlers
│   ├── metrics.py                # Prometheus metrics helpers
│   └── dapr_config.py            # Dapr client factory
│
├── tests/
│   ├── unit/                     # Business logic tests (pytest)
│   │   ├── test_triage_classifier.py
│   │   ├── test_concepts_explainer.py
│   │   └── ...
│   ├── integration/              # Kafka, Dapr, PostgreSQL tests
│   │   ├── test_kafka_pubsub.py
│   │   ├── test_dapr_state.py
│   │   └── test_agent_communication.py
│   ├── contract/                 # API contract validation
│   │   ├── test_triage_api.py
│   │   └── ...
│   └── e2e/                      # Full workflow tests
│       ├── test_student_query_flow.py
│       └── test_multi_agent_workflow.py
│
└── pyproject.toml                # Shared Python tooling config (Black, isort)

# Frontend: Next.js 15 dashboard (EXISTING - mystery-skils-app-ui/)
mystery-skils-app-ui/
├── app/
│   ├── page.tsx                  # Main dashboard (3D Sphere + Terminal + HUD)
│   ├── layout.tsx                # Root layout
│   ├── globals.css               # Global styles + animations
│   └── api/                      # Backend integration (NEW)
│       ├── mastery/
│       │   └── route.ts          # GET /api/mastery - Fetch from Progress Agent (8006)
│       ├── socket/
│       │   └── route.ts          # WebSocket server for real-time agent logs
│       └── auth/
│           └── [...nextauth].ts  # BetterAuth integration (TODO)
│
├── components/ui/                # EXISTING - 3D visualization components
│   ├── MasterySphere.tsx         # 3D Sphere with 7 mastery rings (Three.js)
│   ├── HackerTerminal.tsx        # Real-time agent logs terminal
│   ├── TeacherHUD.tsx            # Student monitoring with struggle detection
│   ├── ChatInterface.tsx         # NEW - Student query submission
│   ├── AgentStatusCards.tsx      # NEW - 6 agent health cards
│   └── MessageFlowViz.tsx        # NEW - Agent-to-agent message visualization
│
├── lib/hooks/                    # EXISTING + NEW
│   ├── useMasteryState.ts        # EXISTING - Mastery data hook (update to fetch from API)
│   ├── useAgentLogs.ts           # EXISTING - WebSocket logs hook (update to connect to backend)
│   ├── useChatSubmit.ts          # NEW - Submit queries to Triage Agent (8001)
│   └── useAgentHealth.ts         # NEW - Fetch agent status from all 6 agents
│
├── lib/api/                      # NEW - Backend API client
│   ├── triageClient.ts           # POST /analyze to port 8001
│   ├── progressClient.ts         # GET /mastery to port 8006
│   └── socketClient.ts           # Socket.io connection to backend WebSocket server
│
├── package.json                  # EXISTING - Dependencies
└── next.config.js                # Next.js config (proxy to backend ports 8001-8006)

# Infrastructure: Kubernetes, Dapr, Kafka
infrastructure/
├── kubernetes/
│   ├── agents/
│   │   ├── triage-deployment.yaml        # Deployment for Triage Agent
│   │   ├── concepts-deployment.yaml
│   │   ├── code-review-deployment.yaml
│   │   ├── debug-deployment.yaml
│   │   ├── exercise-deployment.yaml
│   │   └── progress-deployment.yaml
│   ├── services/
│   │   ├── triage-service.yaml           # ClusterIP service (port 8001)
│   │   ├── concepts-service.yaml
│   │   └── ...
│   └── ingress/
│       └── agents-ingress.yaml           # Ingress routing to all 6 agents
│
├── dapr/
│   ├── components/
│   │   ├── kafka-pubsub.yaml             # Dapr pub/sub component (Kafka)
│   │   ├── postgresql-state.yaml         # Dapr state store component
│   │   └── secrets-store.yaml            # Dapr secrets component (Kubernetes Secrets)
│   └── config/
│       └── config.yaml                   # Dapr global config (tracing, metrics)
│
├── kafka/
│   ├── topics.yaml                       # Kafka topic definitions (student-queries, etc.)
│   └── docker-compose.kafka.yaml         # Local Kafka setup (Zookeeper + Kafka)
│
├── docker-compose.yaml           # Local orchestration (6 agents + Kafka + PostgreSQL)
└── scripts/
    ├── deploy-local.sh           # Minikube deployment script
    ├── verify-agents.py          # Health check validation (~10 token output)
    ├── verify-kafka.py           # Kafka topic validation (~10 token output)
    └── setup-dapr.sh             # Initialize Dapr components

# Documentation
docs/
├── architecture.md               # System architecture diagrams (Mermaid)
├── api-reference/                # Auto-generated API docs (Swagger/OpenAPI)
│   ├── triage.md
│   ├── concepts.md
│   └── ...
└── deployment-guide.md           # Kubernetes deployment instructions

# History
history/
├── prompts/
│   └── 002-learnflow-platform/   # Prompt History Records for this feature
└── adr/                          # Architectural Decision Records
    ├── 001-kafka-vs-rabbitmq.md
    ├── 002-microservices-vs-monolith.md
    └── 003-dapr-state-store-choice.md
```

**Structure Decision**: This is a **web application** with a microservices backend (6 FastAPI agents) and Next.js frontend. The backend follows a multi-service monorepo structure under `backend/agents/` with shared utilities in `backend/shared/`. The frontend is the existing `mystery-skils-app-ui/` directory, which will be extended with new API routes and components to integrate with the backend agents. Infrastructure configuration (Kubernetes, Dapr, Kafka) is centralized in `infrastructure/` for GitOps deployment.

**Real Directories Captured**:
- `backend/` - Exists at repository root
- `mystery-skils-app-ui/` - Exists at repository root (confirmed via ls)
- `infrastructure/` - Exists at repository root
- `docs/` - Exists at repository root
- `history/` - Exists at repository root
- `specs/002-learnflow-platform/` - Exists (current feature)

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| 6 microservices (vs monolith) | Each agent has distinct responsibility (Triage, Concepts, Code Review, Debug, Exercise, Progress); independent scaling needed (e.g., Code Review may have higher load than Exercise Generator); fault isolation (one agent crash doesn't bring down entire system) | Monolithic API with 6 modules: Rejected because (1) cannot scale agents independently (all-or-nothing scaling wastes resources), (2) shared runtime means one agent's Claude API rate limit affects all others, (3) deployment risk (one bug in Code Review agent breaks entire platform) |
| Kafka pub/sub (vs direct HTTP) | Asynchronous communication required for multi-agent workflows (e.g., Triage → Debug → Concepts); decouples agents (no direct dependencies); enables event sourcing for debugging (replay messages); scales horizontally (consumer groups) | Direct HTTP calls between agents: Rejected because (1) tight coupling (Triage must know URLs of all 5 specialists), (2) synchronous blocking (if Concepts Agent is slow, Triage request times out), (3) retry complexity (each agent must implement own retry logic), (4) no audit trail (can't replay student query flow for debugging) |
| Dapr sidecars (vs native SDKs) | Abstracts infrastructure complexity (Kafka, PostgreSQL, secrets) from agent code; enables polyglot future (could add Rust or Go agents); unified observability (Dapr handles tracing); portable across clouds (Dapr components swap without code changes) | Native Kafka/PostgreSQL SDKs in each agent: Rejected because (1) code duplication (6 agents implement same connection pooling, retry logic), (2) vendor lock-in (switching from Kafka to NATS requires rewriting all agents), (3) inconsistent observability (each agent uses different tracing library), (4) higher learning curve for new developers |
| PostgreSQL via Dapr state store (vs direct SQL) | Dapr provides consistent state API across agents; built-in retries, connection pooling; enables swapping to CosmosDB or DynamoDB without code changes; reduces boilerplate (no ORM setup) | Direct PostgreSQL with SQLAlchemy: Rejected because (1) each agent must configure ORM, migrations, connection pooling, (2) schema changes require coordinated migrations across 6 services, (3) testing complexity (need to mock database in unit tests), (4) cloud portability (hard to switch to managed NoSQL later) |
| Claude API at runtime (vs pre-trained local models) | Requires latest Claude model capabilities (coding expertise, reasoning); no GPU infrastructure needed (cost savings); automatic model updates (no retraining); superior response quality compared to open-source models for code review, debugging | Local models (e.g., CodeLlama, Mistral): Rejected because (1) GPU infrastructure cost exceeds Claude API cost at target scale (10k users), (2) model expertise for code review/debugging lags Claude Opus/Sonnet, (3) operational burden (model hosting, scaling, updates), (4) latency (local inference on CPU too slow; GPU adds cost) |

**Justification Summary**: All complexity is driven by **functional requirements** (6 specialist agents, real-time collaboration, independent scaling) and **constitutional principles** (event-driven architecture, cloud-native deployment, AI-native runtime). Each architectural choice prioritizes operational simplicity (Dapr abstracts complexity), scalability (Kafka enables horizontal scaling), and maintainability (microservices enable independent deployments). Simpler alternatives (monolith, direct HTTP, native SDKs, local models) fail on non-functional requirements (latency, fault isolation, scaling efficiency, response quality).
