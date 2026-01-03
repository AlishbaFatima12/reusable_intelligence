# Tasks: LearnFlow Multi-Agent Learning Platform

**Input**: Design documents from `/specs/002-learnflow-platform/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: This project does NOT include automated test generation in initial implementation. Tests can be added in Polish phase if time permits.

**Organization**: Tasks are grouped by user story (US1: AI-Routed Learning, US2: Visual Workflow, US3: Agent Monitoring) to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

Per plan.md, this is a **web application** with:
- **Backend**: `backend/agents/` (6 microservices) + `backend/shared/`
- **Frontend**: `mystery-skils-app-ui/` (Next.js app - ALREADY EXISTS, needs integration)
- **Infrastructure**: `infrastructure/` (Kubernetes, Dapr, Kafka)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, infrastructure configuration, and backend structure

- [x] T001 Create backend directory structure (agents/, shared/, tests/)
- [x] T002 Create infrastructure directory structure (kubernetes/, dapr/, kafka/, scripts/)
- [x] T003 Create root .env.example file with all required environment variables
- [x] T004 Create docker-compose.yaml for local development (Kafka, Zookeeper, PostgreSQL)
- [x] T005 [P] Create backend/requirements.txt with FastAPI, Dapr SDK, Anthropic SDK, Kafka-python, Pydantic
- [x] T006 [P] Create backend/pyproject.toml for Black, isort, pytest configuration
- [x] T007 [P] Create infrastructure/kafka/topics.yaml defining all 7 Kafka topics
- [x] T008 [P] Create infrastructure/dapr/components/kafka-pubsub.yaml for Dapr Kafka pub/sub component
- [x] T009 [P] Create infrastructure/dapr/components/postgresql-state.yaml for Dapr state store component
- [x] T010 [P] Create infrastructure/dapr/components/secrets-store.yaml for Dapr secrets component
- [x] T011 [P] Create infrastructure/dapr/config/config.yaml for Dapr global configuration (tracing, metrics)
- [x] T012 [P] Create infrastructure/scripts/deploy-local.sh for Minikube deployment
- [x] T013 [P] Create infrastructure/scripts/verify-agents.py for agent health validation
- [x] T014 [P] Create infrastructure/scripts/verify-kafka.py for Kafka topic validation

**Checkpoint**: Infrastructure configuration complete - foundation ready for shared code

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared utilities and base classes that ALL agents depend on - MUST complete before any agent implementation

**⚠️ CRITICAL**: No agent work can begin until this phase is complete

- [x] T015 Create backend/shared/__init__.py
- [x] T016 [P] Create backend/shared/models.py with Pydantic models (StudentQuery, AgentResponse, KafkaMessageEnvelope, etc.)
- [x] T017 [P] Create backend/shared/kafka_client.py with Kafka producer/consumer wrappers
- [x] T018 [P] Create backend/shared/dapr_client.py with Dapr state/pub-sub helper functions
- [x] T019 [P] Create backend/shared/claude_client.py with Anthropic API wrapper (rate limiting, retries, error handling)
- [x] T020 [P] Create backend/shared/logging_config.py with structured JSON logging setup
- [x] T021 [P] Create backend/shared/health_checks.py with /health and /ready endpoint handlers
- [x] T022 [P] Create backend/shared/metrics.py with Prometheus metrics helpers
- [x] T023 Create backend/shared/config.py for environment variable loading and validation

**Checkpoint**: Shared utilities ready - agents can now be implemented in parallel

---

## Phase 3: User Story 1 - Student Receives AI-Routed Learning Help (Priority: P1) 🎯 MVP

**Goal**: Student submits query → Triage routes to specialist → Student receives personalized response

**Independent Test**:
```bash
# Submit query via Triage Agent
curl -X POST http://localhost:8001/analyze \
  -d '{"query_id":"test-001","student_id":"s1","query_text":"What is recursion?"}'

# Verify routing decision in Kafka topic: triage-routing
# Verify response generated in Kafka topic: agent-responses
# Expected: Response with explanation and code examples within 5 seconds
```

### Implementation for User Story 1

#### Triage Agent (Port 8001) - Query Routing

- [x] T024 [P] [US1] Create backend/agents/triage/__init__.py
- [x] T025 [P] [US1] Create backend/agents/triage/config.py with environment variables (ANTHROPIC_API_KEY, KAFKA_BOOTSTRAP_SERVERS)
- [x] T026 [P] [US1] Create backend/agents/triage/models.py with QueryAnalysisRequest, QueryAnalysisResponse Pydantic models
- [x] T027 [P] [US1] Create backend/agents/triage/requirements.txt (FastAPI, dapr-sdk, anthropic, kafka-python)
- [x] T028 [P] [US1] Create backend/agents/triage/Dockerfile (multi-stage build for production)
- [x] T029 [US1] Create backend/agents/triage/services/classifier.py with Claude API intent classification logic
- [x] T030 [US1] Create backend/agents/triage/services/publisher.py with Kafka publisher for routing decisions
- [x] T031 [US1] Create backend/agents/triage/routes.py with POST /analyze endpoint (depends on T029, T030)
- [x] T032 [US1] Create backend/agents/triage/main.py with FastAPI app initialization, /health, /ready, /metrics endpoints

#### Concepts Agent (Port 8002) - Concept Explanations

- [x] T033 [P] [US1] Create backend/agents/concepts/__init__.py
- [x] T034 [P] [US1] Create backend/agents/concepts/config.py
- [x] T035 [P] [US1] Create backend/agents/concepts/models.py with ConceptExplanationRequest, ConceptExplanationResponse
- [x] T036 [P] [US1] Create backend/agents/concepts/requirements.txt
- [x] T037 [P] [US1] Create backend/agents/concepts/Dockerfile
- [x] T038 [US1] Create backend/agents/concepts/services/explainer.py with Claude API for generating explanations
- [x] T039 [US1] Create backend/agents/concepts/services/subscriber.py with Kafka subscriber for concepts-queries topic
- [x] T040 [US1] Create backend/agents/concepts/services/state_manager.py with Dapr state store for caching explanations
- [x] T041 [US1] Create backend/agents/concepts/routes.py with POST /explain endpoint
- [x] T042 [US1] Create backend/agents/concepts/main.py with FastAPI app and Kafka consumer startup

#### Code Review Agent (Port 8003) - Code Quality Feedback

- [ ] T043 [P] [US1] Create backend/agents/code-review/__init__.py
- [ ] T044 [P] [US1] Create backend/agents/code-review/config.py
- [ ] T045 [P] [US1] Create backend/agents/code-review/models.py with CodeReviewRequest, CodeReviewResponse
- [ ] T046 [P] [US1] Create backend/agents/code-review/requirements.txt
- [ ] T047 [P] [US1] Create backend/agents/code-review/Dockerfile
- [ ] T048 [US1] Create backend/agents/code-review/services/reviewer.py with Claude API for code analysis
- [ ] T049 [US1] Create backend/agents/code-review/services/subscriber.py with Kafka subscriber
- [ ] T050 [US1] Create backend/agents/code-review/routes.py with POST /review endpoint
- [ ] T051 [US1] Create backend/agents/code-review/main.py with FastAPI app

#### Debug Agent (Port 8004) - Error Diagnosis

- [ ] T052 [P] [US1] Create backend/agents/debug/__init__.py
- [ ] T053 [P] [US1] Create backend/agents/debug/config.py
- [ ] T054 [P] [US1] Create backend/agents/debug/models.py with DiagnosisRequest, DiagnosisResponse
- [ ] T055 [P] [US1] Create backend/agents/debug/requirements.txt
- [ ] T056 [P] [US1] Create backend/agents/debug/Dockerfile
- [ ] T057 [US1] Create backend/agents/debug/services/debugger.py with Claude API for error analysis
- [ ] T058 [US1] Create backend/agents/debug/services/subscriber.py with Kafka subscriber
- [ ] T059 [US1] Create backend/agents/debug/services/error_parser.py for parsing stack traces and syntax errors
- [ ] T060 [US1] Create backend/agents/debug/routes.py with POST /diagnose endpoint
- [ ] T061 [US1] Create backend/agents/debug/main.py with FastAPI app

#### Exercise Generator (Port 8005) - Practice Problems

- [ ] T062 [P] [US1] Create backend/agents/exercise/__init__.py
- [ ] T063 [P] [US1] Create backend/agents/exercise/config.py
- [ ] T064 [P] [US1] Create backend/agents/exercise/models.py with ExerciseGenerationRequest, Exercise
- [ ] T065 [P] [US1] Create backend/agents/exercise/requirements.txt
- [ ] T066 [P] [US1] Create backend/agents/exercise/Dockerfile
- [ ] T067 [US1] Create backend/agents/exercise/services/generator.py with Claude API for creating exercises
- [ ] T068 [US1] Create backend/agents/exercise/services/subscriber.py with Kafka subscriber
- [ ] T069 [US1] Create backend/agents/exercise/services/difficulty_scaler.py for adjusting problem difficulty
- [ ] T070 [US1] Create backend/agents/exercise/routes.py with POST /generate and GET /exercises/{topic} endpoints
- [ ] T071 [US1] Create backend/agents/exercise/main.py with FastAPI app

#### Progress Tracker (Port 8006) - Learning Analytics

- [x] T072 [P] [US1] Create backend/agents/progress/__init__.py
- [x] T073 [P] [US1] Create backend/agents/progress/config.py
- [x] T074 [P] [US1] Create backend/agents/progress/models.py with MasteryResponse, LearningProgress, StruggleDetectionRequest
- [x] T075 [P] [US1] Create backend/agents/progress/requirements.txt
- [x] T076 [P] [US1] Create backend/agents/progress/Dockerfile
- [x] T077 [US1] Create backend/agents/progress/services/tracker.py for tracking student milestones and topics
- [x] T078 [US1] Create backend/agents/progress/services/analytics.py with Claude API for generating learning insights
- [x] T079 [US1] Create backend/agents/progress/services/subscriber.py to subscribe to all agent-responses
- [x] T080 [US1] Create backend/agents/progress/services/state_manager.py with Dapr state store for student progress
- [x] T081 [US1] Create backend/agents/progress/routes.py with GET /mastery/{student_id}, POST /mastery/{student_id}, GET /insights/{student_id}, POST /struggle-detection
- [x] T082 [US1] Create backend/agents/progress/main.py with FastAPI app

**Checkpoint**: At this point, User Story 1 should be fully functional - all 6 agents can route queries and generate responses

---

## Phase 4: User Story 2 - Visual Agent Workflow Transparency (Priority: P2)

**Goal**: Students can see which agent is handling their question and watch the message flow between agents

**Independent Test**:
```bash
# Submit complex query
curl -X POST http://localhost:8001/analyze \
  -d '{"query_id":"test-002","student_id":"s1","query_text":"Debug this code"}'

# Open Mystery Skills UI at http://localhost:4000
# Expected:
# - Hacker Terminal shows "Triage Agent: Analyzing query..." log
# - Message Flow visualization shows routing from Triage → Debug
# - Agent Status Card shows "Debug Agent: Processing..." status
# - Response appears in chat with "Answered by: Debug Agent"
```

### Implementation for User Story 2

#### Frontend Integration with Mystery Skills UI

- [ ] T083 [P] [US2] Create mystery-skils-app-ui/app/api/query/route.ts with POST endpoint to Triage Agent (http://localhost:8001/analyze)
- [ ] T084 [P] [US2] Create mystery-skils-app-ui/lib/api/triageClient.ts with fetch wrapper for Triage API
- [ ] T085 [P] [US2] Create mystery-skils-app-ui/lib/hooks/useChatSubmit.ts for submitting queries from chat interface
- [ ] T086 [P] [US2] Create mystery-skils-app-ui/components/ui/ChatInterface.tsx with query input, submit button, response display
- [ ] T087 [P] [US2] Create mystery-skils-app-ui/components/ui/AgentStatusCards.tsx showing 6 agent health cards with status (active/idle/degraded/error)
- [ ] T088 [P] [US2] Create mystery-skils-app-ui/lib/hooks/useAgentHealth.ts to poll all 6 agent /health endpoints every 5 seconds
- [ ] T089 [P] [US2] Create mystery-skils-app-ui/components/ui/MessageFlowViz.tsx to visualize Triage → Specialist routing with animated arrows
- [ ] T090 [US2] Update mystery-skils-app-ui/lib/hooks/useAgentLogs.ts to connect to WebSocket server (replace simulated data)
- [ ] T091 [US2] Update mystery-skils-app-ui/app/page.tsx to include ChatInterface and AgentStatusCards components

#### WebSocket Server for Real-Time Updates

- [ ] T092 [US2] Create mystery-skils-app-ui/app/api/socket/route.ts with Socket.io server for real-time agent logs
- [ ] T093 [US2] Create backend/websocket-bridge/main.py with Kafka consumer subscribing to agent-logs, agent-status topics
- [ ] T094 [US2] Update backend/websocket-bridge/main.py to publish Kafka messages to Socket.io rooms (socket.emit('agent-log', ...))
- [ ] T095 [US2] Create backend/websocket-bridge/Dockerfile for WebSocket bridge service
- [ ] T096 [US2] Create backend/websocket-bridge/requirements.txt with python-socketio, kafka-python

#### Agent Logging Updates

- [ ] T097 [P] [US2] Update backend/agents/triage/routes.py to publish "Analyzing query..." log to agent-logs Kafka topic
- [ ] T098 [P] [US2] Update backend/agents/triage/services/publisher.py to publish "Routing to {agent}" log
- [ ] T099 [P] [US2] Update backend/agents/concepts/services/explainer.py to publish "Generating explanation..." log
- [ ] T100 [P] [US2] Update backend/agents/code-review/services/reviewer.py to publish "Analyzing code..." log
- [ ] T101 [P] [US2] Update backend/agents/debug/services/debugger.py to publish "Diagnosing error..." log
- [ ] T102 [P] [US2] Update backend/agents/exercise/services/generator.py to publish "Creating exercises..." log
- [ ] T103 [P] [US2] Update backend/agents/progress/services/tracker.py to publish "Updating progress..." log

#### Agent Status Heartbeat

- [ ] T104 [P] [US2] Add heartbeat publisher to backend/agents/triage/main.py (publish to agent-status topic every 10 seconds)
- [ ] T105 [P] [US2] Add heartbeat publisher to backend/agents/concepts/main.py
- [ ] T106 [P] [US2] Add heartbeat publisher to backend/agents/code-review/main.py
- [ ] T107 [P] [US2] Add heartbeat publisher to backend/agents/debug/main.py
- [ ] T108 [P] [US2] Add heartbeat publisher to backend/agents/exercise/main.py
- [ ] T109 [P] [US2] Add heartbeat publisher to backend/agents/progress/main.py

**Checkpoint**: At this point, User Stories 1 AND 2 work - students can submit queries and see real-time agent activity

---

## Phase 5: User Story 3 - Real-Time Agent Health Monitoring (Priority: P3)

**Goal**: Instructors/admins can monitor status of all 6 agents in real-time, seeing which are active/idle/error

**Independent Test**:
```bash
# Open Mystery Skills UI at http://localhost:4000
# Expected:
# - 6 Agent Status Cards showing: Triage (Active), Concepts (Idle), Code Review (Idle), Debug (Active), Exercise (Idle), Progress (Active)
# - Each card shows: uptime, last activity timestamp, current queue depth
# - If agent crashes: Status changes to "Error" with red indicator
# - If agent restarts: Status changes back to "Active" and uptime resets
```

### Implementation for User Story 3

#### Agent Health Metrics Collection

- [ ] T110 [P] [US3] Update backend/shared/health_checks.py to include uptime tracking, last_activity timestamp
- [ ] T111 [P] [US3] Update backend/shared/metrics.py to track queue_depth, total_queries_processed, error_count
- [ ] T112 [US3] Update backend/agents/triage/routes.py /ready endpoint to check Kafka and Dapr connectivity
- [ ] T113 [US3] Update backend/agents/concepts/routes.py /ready endpoint to check dependencies
- [ ] T114 [US3] Update backend/agents/code-review/routes.py /ready endpoint
- [ ] T115 [US3] Update backend/agents/debug/routes.py /ready endpoint
- [ ] T116 [US3] Update backend/agents/exercise/routes.py /ready endpoint
- [ ] T117 [US3] Update backend/agents/progress/routes.py /ready endpoint

#### Kubernetes Health Probes (Optional - for production deployment)

- [ ] T118 [P] [US3] Create infrastructure/kubernetes/agents/triage-deployment.yaml with liveness/readiness probes
- [ ] T119 [P] [US3] Create infrastructure/kubernetes/agents/concepts-deployment.yaml
- [ ] T120 [P] [US3] Create infrastructure/kubernetes/agents/code-review-deployment.yaml
- [ ] T121 [P] [US3] Create infrastructure/kubernetes/agents/debug-deployment.yaml
- [ ] T122 [P] [US3] Create infrastructure/kubernetes/agents/exercise-deployment.yaml
- [ ] T123 [P] [US3] Create infrastructure/kubernetes/agents/progress-deployment.yaml

#### Frontend Monitoring Dashboard Enhancements

- [ ] T124 [US3] Update mystery-skils-app-ui/lib/hooks/useAgentHealth.ts to parse uptime, queue_depth, error_count from /health responses
- [ ] T125 [US3] Update mystery-skils-app-ui/components/ui/AgentStatusCards.tsx to display detailed metrics (uptime, queue, errors)
- [ ] T126 [US3] Add error state visualization to AgentStatusCards (red indicator, error message display)
- [ ] T127 [US3] Add idle state detection (no activity for 60+ seconds) with yellow indicator

**Checkpoint**: All user stories (US1, US2, US3) are now complete and independently functional

---

## Phase 6: Mystery Skills UI - Mastery Tracking Integration

**Goal**: Connect existing 3D Mastery Sphere and Teacher HUD to backend Progress Tracker

**Independent Test**:
```bash
# Submit 5 successful queries on "Functions" topic
# Open Mystery Skills UI at http://localhost:4000
# Expected:
# - 3D Sphere "Functions" ring changes color from Red (0%) → Orange (33%)
# - Progress bar updates in real-time
# - After 10 queries: Ring turns Green (66%)
# - After completing all exercises: Ring turns Blue (100%)

# Submit 6 failed runs on "OOP Basics"
# Expected:
# - Teacher HUD shows student card with pulsing RED alert
# - Card displays: "Student_123 - 6 failed runs - OOP Basics"
```

### Implementation

- [ ] T128 [P] Create mystery-skils-app-ui/app/api/mastery/route.ts with GET endpoint fetching from Progress Tracker (http://localhost:8006/mastery/{student_id})
- [ ] T129 [P] Create mystery-skils-app-ui/lib/api/progressClient.ts with fetch wrapper for Progress Tracker API
- [ ] T130 Update mystery-skils-app-ui/lib/hooks/useMasteryState.ts to fetch from /api/mastery instead of simulated data
- [ ] T131 Update backend/websocket-bridge/main.py to subscribe to mastery-updates and student-struggle Kafka topics
- [ ] T132 Update backend/websocket-bridge/main.py to emit 'mastery-update' and 'student-struggle' events to Socket.io
- [ ] T133 Update mystery-skils-app-ui/components/ui/MasterySphere.tsx to listen for mastery-update Socket.io events
- [ ] T134 Update mystery-skils-app-ui/components/ui/TeacherHUD.tsx to listen for student-struggle Socket.io events
- [ ] T135 Update backend/agents/progress/services/tracker.py to publish mastery-updates to Kafka when progress changes
- [ ] T136 Update backend/agents/progress/routes.py POST /struggle-detection to publish student-struggle events when failedRuns >= 5

**Checkpoint**: Mystery Skills UI is now fully connected to backend - real-time mastery tracking and struggle detection working

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, testing, optimization, and deployment preparation

- [ ] T137 [P] Create docs/architecture.md with system architecture diagrams (Mermaid)
- [ ] T138 [P] Create docs/api-reference/ directory with links to OpenAPI specs for all 6 agents
- [ ] T139 [P] Create docs/deployment-guide.md with Kubernetes deployment instructions
- [ ] T140 [P] Update README.md with project overview, quickstart link, architecture diagram
- [ ] T141 [P] Create .dockerignore files for all agent Dockerfiles
- [ ] T142 [P] Create .gitignore with Python, Node.js, environment variables, Docker, Kubernetes patterns
- [ ] T143 Run infrastructure/scripts/verify-agents.py to validate all 6 agents are healthy
- [ ] T144 Run infrastructure/scripts/verify-kafka.py to validate all 7 Kafka topics exist
- [ ] T145 Test end-to-end flow per quickstart.md: submit query → verify routing → verify response → verify UI updates
- [ ] T146 [P] Add rate limiting middleware to all agent /analyze, /review, /diagnose, /generate endpoints
- [ ] T147 [P] Add request logging to all agents (log query_id, student_id, processing_time_ms)
- [ ] T148 [P] Add CORS configuration to all agent FastAPI apps for frontend access
- [ ] T149 Create AGENTS.md via agents-md-gen skill (auto-generate from FastAPI code)
- [ ] T150 Create history/adr/001-kafka-vs-rabbitmq.md documenting why Kafka was chosen
- [ ] T151 Create history/adr/002-microservices-vs-monolith.md documenting architectural decision
- [ ] T152 Create history/adr/003-dapr-state-store-choice.md documenting PostgreSQL via Dapr decision
- [ ] T153 Run npm run build in mystery-skils-app-ui to verify production build succeeds
- [ ] T154 [P] Create infrastructure/kubernetes/services/ with ClusterIP services for all 6 agents
- [ ] T155 [P] Create infrastructure/kubernetes/ingress/agents-ingress.yaml for routing to agents
- [ ] T156 [P] Create infrastructure/kubernetes/postgres-deployment.yaml
- [ ] T157 [P] Create infrastructure/kubernetes/kafka-deployment.yaml
- [ ] T158 [P] Create infrastructure/kubernetes/namespace.yaml for learnflow namespace
- [ ] T159 Create .github/workflows/test-agents.yml for pytest CI pipeline
- [ ] T160 Create .github/workflows/build-images.yml for Docker image builds
- [ ] T161 Create .github/workflows/deploy-k8s.yml for ArgoCD GitOps deployment
- [ ] T162 Run quickstart.md validation: follow all steps, verify system works end-to-end

**Checkpoint**: System is production-ready, documented, and deployable to Kubernetes

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories and agents
- **User Story 1 (Phase 3)**: Depends on Foundational completion - All 6 agents can be built in parallel
- **User Story 2 (Phase 4)**: Depends on User Story 1 completion (needs agents running to display activity)
- **User Story 3 (Phase 5)**: Depends on User Story 1 completion (needs agents to monitor health)
- **Mastery Integration (Phase 6)**: Depends on User Story 1 completion (needs Progress Tracker agent)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories ✅ MVP
- **User Story 2 (P2)**: Depends on US1 agents running - Adds real-time visualization
- **User Story 3 (P3)**: Depends on US1 agents running - Adds monitoring dashboard
- **Mastery Integration**: Depends on US1 Progress Tracker - Connects existing Mystery Skills UI

### Within Each User Story

**User Story 1** (6 agents):
1. All agent directories can be created in parallel (T024-T082)
2. Within each agent: config.py and models.py before services
3. Services before routes.py
4. Routes before main.py

**User Story 2** (Real-time visualization):
1. Frontend API routes [P] in parallel
2. WebSocket bridge after Kafka topics exist
3. Agent logging updates [P] in parallel
4. Heartbeat publishers [P] in parallel

**User Story 3** (Health monitoring):
1. Health metrics updates [P] in parallel
2. Kubernetes manifests [P] in parallel (optional)
3. Frontend monitoring enhancements after health metrics ready

### Parallel Opportunities

- **Setup Phase**: Tasks T003-T014 marked [P] can run in parallel (11 tasks)
- **Foundational Phase**: Tasks T016-T022 marked [P] can run in parallel (7 tasks)
- **User Story 1**:
  - All 6 agent __init__.py files [P] (T024, T033, T043, T052, T062, T072)
  - All 6 agent config.py files [P] (T025, T034, T044, T053, T063, T073)
  - All 6 agent models.py files [P] (T026, T035, T045, T054, T064, T074)
  - All 6 agent requirements.txt [P] (T027, T036, T046, T055, T065, T075)
  - All 6 agent Dockerfiles [P] (T028, T037, T047, T056, T066, T076)
  - **Total: ~30 parallel tasks within US1**
- **User Story 2**:
  - Frontend components [P] (T083-T089)
  - Agent logging updates [P] (T097-T103)
  - Heartbeat publishers [P] (T104-T109)
- **Polish Phase**: Documentation [P] (T137-T140), Kubernetes manifests [P] (T154-T158)

---

## Parallel Example: User Story 1 - All 6 Agents

```bash
# Phase 1: Create all agent structures in parallel (30 tasks)
Task: "Create backend/agents/triage/__init__.py" [T024]
Task: "Create backend/agents/concepts/__init__.py" [T033]
Task: "Create backend/agents/code-review/__init__.py" [T043]
Task: "Create backend/agents/debug/__init__.py" [T052]
Task: "Create backend/agents/exercise/__init__.py" [T062]
Task: "Create backend/agents/progress/__init__.py" [T072]
# ... repeat for config.py, models.py, requirements.txt, Dockerfile

# Phase 2: Implement services sequentially per agent (but agents parallel)
# Agent 1 (Triage): T029 → T030 → T031 → T032
# Agent 2 (Concepts): T038 → T039 → T040 → T041 → T042
# Agent 3 (Code Review): T048 → T049 → T050 → T051
# Agent 4 (Debug): T057 → T058 → T059 → T060 → T061
# Agent 5 (Exercise): T067 → T068 → T069 → T070 → T071
# Agent 6 (Progress): T077 → T078 → T079 → T080 → T081 → T082
```

---

## Implementation Strategy

### MVP First (User Story 1 Only) - RECOMMENDED FOR HACKATHON

1. Complete Phase 1: Setup (T001-T014) - ~30 minutes
2. Complete Phase 2: Foundational (T015-T023) - ~45 minutes
3. Complete Phase 3: User Story 1 (T024-T082) - **~3-4 hours** (all 6 agents)
4. **STOP and VALIDATE**: Test User Story 1 independently via cURL
5. **Demo**: Show query routing, agent responses, Claude API integration

**Time Estimate for MVP**: ~5 hours

### Full Hackathon Delivery

1. Complete Setup + Foundational → Foundation ready (~1.5 hours)
2. Complete User Story 1 → Test independently → **MVP CHECKPOINT** (~3-4 hours)
3. Complete User Story 2 → Add real-time visualization (~1 hour)
4. Complete Mastery Integration (Phase 6) → Connect Mystery Skills UI (~30 min)
5. Complete Polish (Phase 7) → Documentation, deployment prep (~1 hour)

**Total Time Estimate**: ~7-8 hours for complete system

### Parallel Team Strategy

With 3 developers:

1. **All together**: Complete Setup + Foundational (T001-T023)
2. **Split User Story 1**:
   - Developer A: Triage + Concepts agents (T024-T042)
   - Developer B: Code Review + Debug agents (T043-T061)
   - Developer C: Exercise + Progress agents (T062-T082)
3. **Reconverge**: Test US1 together
4. **Developer A**: User Story 2 (T083-T109)
5. **Developer B**: Mastery Integration (T128-T136)
6. **Developer C**: Polish (T137-T162)

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [US1], [US2], [US3] labels map tasks to specific user stories
- Each user story should be independently completable and testable
- **Tests NOT included**: Can be added later in polish phase if time permits
- Commit after each logical task group (e.g., after completing each agent)
- Stop at any checkpoint to validate story independently
- **Backend focus**: All 6 agents (T024-T082) are the core implementation
- **Frontend integration**: Only T083-T136 needed to connect existing Mystery Skills UI
- **Production deployment**: Phase 7 tasks (T137-T162) are optional for hackathon demo

---

## Task Count Summary

- **Phase 1 (Setup)**: 14 tasks
- **Phase 2 (Foundational)**: 9 tasks
- **Phase 3 (User Story 1)**: 59 tasks (6 agents × ~10 tasks each)
- **Phase 4 (User Story 2)**: 27 tasks (Frontend + WebSocket + Logging)
- **Phase 5 (User Story 3)**: 18 tasks (Health monitoring)
- **Phase 6 (Mastery Integration)**: 9 tasks (3D Sphere + Teacher HUD)
- **Phase 7 (Polish)**: 26 tasks (Documentation, deployment, CI/CD)

**TOTAL**: 162 tasks

**Parallel Opportunities**: ~60 tasks can run in parallel (37% of total)

**MVP Scope (US1 only)**: 82 tasks (~5 hours)

**Full System**: 162 tasks (~7-8 hours)
