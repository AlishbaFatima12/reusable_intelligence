# Implementation Plan: Mystery Skills - The Learning Revolution
## Hackathon III: Reusable Intelligence & Cloud-Native Mastery

**Created:** 2025-12-29
**Author:** Syeda Alishba Fatima
**Status:** Phase 0 - Planning
**Branch:** master (will create feature branches per phase)

---

## Executive Summary

**Project**: Mystery Skills - The Learning Revolution
**Original Name**: LearnFlow (rebranded for differentiation)
**Type**: AI-Powered Python Learning Platform with Multi-Agent Architecture

**Goal**: Build a production-ready, cloud-native learning platform using agent-native development principles, demonstrating 99.3% token efficiency through reusable skills.

**Success Criteria**:
- ✅ 85/100+ hackathon score (Top Tier)
- ✅ Single-prompt deployment (Skills Autonomy: 15/15)
- ✅ 99.3% token reduction (Token Efficiency: 10/10)
- ✅ Works on Claude Code AND Goose (Cross-Agent: 5/5)
- ✅ Event-driven architecture (Architecture: 18/20)
- ✅ All 6 AI agents operational (LearnFlow Completion: 15/15)

---

## Constitution Check

### Alignment with Core Principles

**I. Agent-Native Development** ✅
- Skills will be the primary product
- Agents (Claude Code + Goose) will generate all implementation code
- Single-prompt deployment target for each component
- Intent-based skill instructions (not step-by-step)

**II. Token Efficiency** ✅
- Target: <780 tokens total deployment (vs 115,000 traditional)
- MCP Code Execution Pattern for all infrastructure operations
- Validation scripts return ~10 tokens (not 5000)
- No raw data dumps in agent context

**III. Spec-Driven Development** ✅
- This plan.md precedes all implementation
- Specifications for each agent service defined below
- Acceptance criteria for each component
- Agents will make autonomous decisions based on specs

**IV. Skills as Permanent Knowledge** ✅
- 7 reusable skills to be created
- Cross-agent compatible (tested on Claude + Goose)
- Skills will work across multiple projects
- Token cost <150 per skill

**V. Event-Driven Cloud-Native** ✅
- Kafka pub/sub for agent communication
- Dapr sidecars for state/secrets/service invocation
- Stateless microservices (FastAPI)
- Kubernetes orchestration (Minikube → Cloud)

**VI. AI-Native Runtime** ✅
- LearnFlow agents use Claude API at runtime
- Not just build-time automation
- Agents learn from interactions (vector DB)
- Self-healing via K8s probes

**VII. Testing & Validation** ✅
- Every skill includes validation scripts
- Automated verification (no manual checks)
- CI pipeline with tests

**VIII. Documentation as Code** ✅
- AGENTS.md auto-generated via skill
- API docs via Docusaurus
- ADRs for architectural decisions

---

## Phase 0: Research & Technical Context

### Technology Stack (Finalized)

**Frontend**:
- Framework: Next.js 14+ (App Router)
- UI Library: React 19
- Styling: Tailwind CSS + Custom CSS (from existing UI)
- Code Editor: Monaco Editor (VS Code engine)
- 3D Graphics: Three.js / React Three Fiber (for Mastery Sphere)
- Animations: Framer Motion + CSS animations
- State Management: React Context + Zustand (lightweight)
- Auth: Better Auth (modern, type-safe)

**Backend**:
- Language: Python 3.11+
- Framework: FastAPI (async, high-performance)
- Sidecar: Dapr 1.12+ (pub/sub, state, secrets)
- Message Queue: Apache Kafka (via Bitnami Helm)
- Database: PostgreSQL 15+ (via Bitnami Helm)
- ORM: SQLAlchemy 2.0 (async)
- Validation: Pydantic 2.5+
- AI Integration: Anthropic Claude API (Claude Sonnet 4.5)

**Infrastructure**:
- Orchestration: Kubernetes 1.28+ (Minikube local)
- Package Manager: Helm 3.13+
- Service Mesh: Dapr (lightweight alternative to Istio)
- API Gateway: Kong (optional, may use K8s Ingress)
- CI: GitHub Actions
- CD: ArgoCD (GitOps)

**Observability**:
- Logging: Structured JSON (Python logging module)
- Metrics: Prometheus (via Dapr)
- Tracing: Jaeger/Zipkin (via Dapr)
- Health Checks: FastAPI /health endpoints

**Development Tools**:
- Claude Code (primary agent)
- Goose (cross-agent validation)
- Docker Desktop (container runtime)
- Minikube (local K8s cluster)

### Research Decisions

**Decision 1: Why Dapr over raw Kubernetes?**
- **Rationale**: Dapr provides pub/sub, state management, service invocation, and secrets as sidecar patterns. This reduces boilerplate in each microservice by ~70%.
- **Alternatives Considered**: Direct Kafka client libraries, raw K8s ConfigMaps
- **Trade-off**: Additional component (Dapr runtime), but massive simplification

**Decision 2: Why FastAPI over Flask/Django?**
- **Rationale**: Async support, automatic OpenAPI docs, Pydantic validation, modern Python features
- **Alternatives Considered**: Flask (too basic), Django (too heavyweight)
- **Trade-off**: Smaller community than Flask, but better performance and developer experience

**Decision 3: Why Next.js over pure React?**
- **Rationale**: Server-side rendering, API routes, built-in routing, production optimizations
- **Alternatives Considered**: Vite + React Router, Remix
- **Trade-off**: Some vendor lock-in, but faster development

**Decision 4: Why Monorepo vs Polyrepo?**
- **Rationale**: MONOREPO - Easier cross-service changes, single source of truth, simpler CI/CD
- **Structure**: `backend/<service>/`, `frontend/`, `infrastructure/`, `.claude/skills/`
- **Trade-off**: Larger repo size, but better coordination

**Decision 5: Code Sandbox Implementation**
- **Rationale**: Use RestrictedPython + Docker container with resource limits
- **Security**: No file system access (except temp), no network, 5s timeout, 50MB memory
- **Alternatives Considered**: PyPy sandbox (deprecated), VM-based (too heavy)

---

## Phase 1: Architecture & Design

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Student/Teacher UI                       │
│                    (Next.js + Monaco Editor)                     │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTPS
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Kong API Gateway                            │
│                  (Authentication + Rate Limiting)                │
└────────────────────────┬────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ↓               ↓               ↓
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Triage    │  │  Concepts   │  │ Code Review │
│   Agent     │  │   Agent     │  │   Agent     │
│  (FastAPI)  │  │  (FastAPI)  │  │  (FastAPI)  │
│  + Dapr     │  │  + Dapr     │  │  + Dapr     │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │
       └────────────────┼────────────────┘
                        ↓
              ┌──────────────────┐
              │  Kafka Cluster   │
              │  Topics:         │
              │  - query.received│
              │  - query.routed  │
              │  - response.ready│
              └────────┬─────────┘
                       │
       ┌───────────────┼───────────────┐
       ↓               ↓               ↓
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Debug     │  │  Exercise   │  │  Progress   │
│   Agent     │  │   Agent     │  │   Agent     │
│  (FastAPI)  │  │  (FastAPI)  │  │  (FastAPI)  │
│  + Dapr     │  │  + Dapr     │  │  + Dapr     │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │
       └────────────────┼────────────────┘
                        ↓
              ┌──────────────────┐
              │   PostgreSQL     │
              │   (via Dapr      │
              │   State Store)   │
              └──────────────────┘
```

### Data Model

#### Entities

**1. User**
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('student', 'teacher')),
    full_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

**2. Student Profile**
```sql
CREATE TABLE student_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    current_module VARCHAR(50), -- e.g., 'control_flow'
    overall_mastery_score DECIMAL(5,2) DEFAULT 0.00, -- 0.00 to 100.00
    streak_days INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id)
);
```

**3. Module Progress**
```sql
CREATE TABLE module_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES student_profiles(id) ON DELETE CASCADE,
    module_name VARCHAR(50) NOT NULL, -- 'basics', 'control_flow', etc.
    mastery_score DECIMAL(5,2) DEFAULT 0.00,
    exercise_completion DECIMAL(5,2) DEFAULT 0.00, -- 40% weight
    quiz_scores DECIMAL(5,2) DEFAULT 0.00, -- 30% weight
    code_quality DECIMAL(5,2) DEFAULT 0.00, -- 20% weight
    consistency DECIMAL(5,2) DEFAULT 0.00, -- 10% weight (streak)
    mastery_level VARCHAR(20), -- 'beginner', 'learning', 'proficient', 'mastered'
    color_code VARCHAR(10), -- 'red', 'yellow', 'green', 'blue'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(student_id, module_name)
);
```

**4. Query History**
```sql
CREATE TABLE query_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES student_profiles(id) ON DELETE CASCADE,
    query_text TEXT NOT NULL,
    routed_to_agent VARCHAR(50) NOT NULL, -- 'triage', 'concepts', 'debug', etc.
    response_text TEXT,
    confidence_score DECIMAL(3,2), -- 0.00 to 1.00
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

**5. Code Executions**
```sql
CREATE TABLE code_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES student_profiles(id) ON DELETE CASCADE,
    code_text TEXT NOT NULL,
    execution_result TEXT,
    success BOOLEAN NOT NULL,
    error_type VARCHAR(100), -- e.g., 'SyntaxError', 'NameError'
    execution_time_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

**6. Exercises**
```sql
CREATE TABLE exercises (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    module_name VARCHAR(50) NOT NULL,
    difficulty_level VARCHAR(20) NOT NULL, -- 'easy', 'medium', 'hard'
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    starter_code TEXT,
    solution_code TEXT,
    test_cases JSONB NOT NULL, -- Array of {input, expected_output}
    created_by UUID REFERENCES users(id), -- teacher who created it
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

**7. Exercise Submissions**
```sql
CREATE TABLE exercise_submissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    exercise_id UUID REFERENCES exercises(id) ON DELETE CASCADE,
    student_id UUID REFERENCES student_profiles(id) ON DELETE CASCADE,
    submitted_code TEXT NOT NULL,
    passed_tests INTEGER NOT NULL,
    total_tests INTEGER NOT NULL,
    score DECIMAL(5,2), -- 0.00 to 100.00
    feedback TEXT, -- From Code Review Agent
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

**8. Struggle Alerts**
```sql
CREATE TABLE struggle_alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES student_profiles(id) ON DELETE CASCADE,
    trigger_type VARCHAR(50) NOT NULL, -- 'same_error_3x', 'stuck_10_min', etc.
    context JSONB NOT NULL, -- Details about what triggered the alert
    resolved BOOLEAN DEFAULT FALSE,
    resolved_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### API Contracts

#### Triage Agent API

**Endpoint**: `POST /api/v1/triage/route-query`

**Request**:
```json
{
  "user_id": "uuid",
  "query": "How do for loops work in Python?",
  "context": {
    "current_module": "control_flow",
    "recent_errors": []
  }
}
```

**Response**:
```json
{
  "routed_to": "concepts",
  "confidence": 0.95,
  "reasoning": "Query is asking for concept explanation, no error debugging needed"
}
```

#### Concepts Agent API

**Endpoint**: `POST /api/v1/concepts/explain`

**Request**:
```json
{
  "user_id": "uuid",
  "topic": "for loops",
  "skill_level": "beginner",
  "context": {
    "mastery_score": 0.60
  }
}
```

**Response**:
```json
{
  "explanation": "A for loop in Python...",
  "code_examples": ["for i in range(5): print(i)"],
  "visualization_url": "https://...",
  "related_topics": ["while loops", "range function"]
}
```

#### Debug Agent API

**Endpoint**: `POST /api/v1/debug/analyze`

**Request**:
```json
{
  "user_id": "uuid",
  "code": "for i in rang(5): print(i)",
  "error": "NameError: name 'rang' is not defined",
  "context": {
    "module": "control_flow",
    "attempt_number": 2
  }
}
```

**Response**:
```json
{
  "error_type": "NameError",
  "root_cause": "Typo in function name",
  "hint": "Did you mean 'range' instead of 'rang'?",
  "solution": "for i in range(5): print(i)",
  "explanation": "The range() function is built-in..."
}
```

#### Code Review Agent API

**Endpoint**: `POST /api/v1/code-review/analyze`

**Request**:
```json
{
  "user_id": "uuid",
  "code": "x=5\nprint(x)",
  "context": {
    "module": "basics"
  }
}
```

**Response**:
```json
{
  "correctness": {
    "score": 1.0,
    "issues": []
  },
  "style": {
    "score": 0.8,
    "issues": [
      {
        "line": 1,
        "type": "whitespace",
        "message": "PEP 8: Use spaces around assignment (x = 5)",
        "suggestion": "x = 5"
      }
    ]
  },
  "efficiency": {
    "score": 1.0,
    "issues": []
  },
  "readability": {
    "score": 0.9,
    "issues": []
  },
  "overall_score": 0.925
}
```

#### Exercise Agent API

**Endpoint**: `POST /api/v1/exercise/generate`

**Request**:
```json
{
  "teacher_id": "uuid",
  "module": "data_structures",
  "topic": "list comprehensions",
  "difficulty": "easy",
  "count": 3
}
```

**Response**:
```json
{
  "exercises": [
    {
      "id": "uuid",
      "title": "Basic List Comprehension",
      "description": "Create a list of squares...",
      "starter_code": "# Your code here\n",
      "test_cases": [...]
    }
  ]
}
```

**Endpoint**: `POST /api/v1/exercise/submit`

**Request**:
```json
{
  "student_id": "uuid",
  "exercise_id": "uuid",
  "code": "squares = [x**2 for x in range(10)]"
}
```

**Response**:
```json
{
  "passed": true,
  "tests_passed": 5,
  "tests_total": 5,
  "score": 100.0,
  "feedback": "Excellent! Your list comprehension is correct and follows PEP 8 style."
}
```

#### Progress Agent API

**Endpoint**: `GET /api/v1/progress/student/{student_id}`

**Response**:
```json
{
  "overall_mastery": 0.68,
  "modules": [
    {
      "name": "basics",
      "mastery_score": 0.85,
      "mastery_level": "proficient",
      "color_code": "green"
    },
    {
      "name": "control_flow",
      "mastery_score": 0.60,
      "mastery_level": "learning",
      "color_code": "yellow"
    }
  ],
  "streak_days": 7,
  "recent_activity": [...]
}
```

---

## Phase 2: Skills Required

### Skill Inventory

| # | Skill Name | Purpose | Token Budget | Priority | Status |
|---|------------|---------|--------------|----------|--------|
| 1 | `agents-md-gen` | Generate AGENTS.md for repositories | 100 | HIGH | 📋 Planned |
| 2 | `kafka-k8s-setup` | Deploy Kafka cluster to K8s | 110 | CRITICAL | 📋 Planned |
| 3 | `postgres-k8s-setup` | Deploy PostgreSQL to K8s | 105 | CRITICAL | 📋 Planned |
| 4 | `dapr-setup` | Configure Dapr components | 95 | CRITICAL | 📋 Planned |
| 5 | `fastapi-dapr-agent` | Create FastAPI microservice with Dapr | 120 | CRITICAL | 📋 Planned |
| 6 | `nextjs-k8s-deploy` | Deploy Next.js app to K8s | 115 | HIGH | 📋 Planned |
| 7 | `mcp-code-execution` | MCP with code execution pattern | 95 | MEDIUM | 📋 Planned |
| 8 | `docusaurus-deploy` | Deploy documentation site | 100 | LOW | 📋 Future |

**Total Token Budget**: 840 tokens (vs 115,000 traditional = 99.3% reduction)

### Skill Specifications

#### Skill 1: agents-md-gen

**File**: `.claude/skills/agents-md-gen/SKILL.md`

**Purpose**: Generate comprehensive AGENTS.md files for repositories

**When to Use**:
- New repository needs agent-friendly documentation
- Existing project requires AGENTS.md
- Team adopting agentic development workflow

**What It Does**:
1. Analyzes repository structure (directories, files, tech stack)
2. Generates AGENTS.md with:
   - Repository structure overview
   - Coding conventions and standards
   - Build and deployment processes
   - Testing strategies
   - Common tasks and workflows

**Instructions**:
```bash
python scripts/analyze_repo.py .
python scripts/generate_agents_md.py . > AGENTS.md
python scripts/validate_agents_md.py AGENTS.md
```

**Expected Output**: `✓ AGENTS.md generated: 156 lines`

**Token Cost**: ~100 tokens

---

#### Skill 2: kafka-k8s-setup

**File**: `.claude/skills/kafka-k8s-setup/SKILL.md`

**Purpose**: Deploy Apache Kafka to Kubernetes with verification

**When to Use**:
- Deploying event-driven microservices
- Need message queue for async communication
- Building Mystery Skills backend infrastructure

**What It Does**:
1. Deploys Kafka + Zookeeper to Kubernetes (Bitnami Helm chart)
2. Creates namespace and configures resources
3. Verifies all pods are running
4. Creates test topic to confirm functionality

**Instructions**:
```bash
bash scripts/deploy.sh
python scripts/verify.py
bash scripts/create_test_topic.sh
```

**Configuration**:
- Namespace: `kafka`
- Replicas: 1 (development), 3 (production)
- Zookeeper Replicas: 1 (development), 3 (production)

**Expected Output**: `✓ Kafka deployed to namespace 'kafka' | ✓ All 3 pods running`

**Token Cost**: ~110 tokens

---

#### Skill 3: postgres-k8s-setup

**File**: `.claude/skills/postgres-k8s-setup/SKILL.md`

**Purpose**: Deploy PostgreSQL to Kubernetes with schema migrations

**When to Use**:
- Need relational database for Mystery Skills
- Storing user data, progress, quiz results
- Microservices require persistent storage

**What It Does**:
1. Deploys PostgreSQL to Kubernetes (Bitnami Helm chart)
2. Creates database and user
3. Runs schema migrations (from `migrations/` folder)
4. Verifies connectivity

**Instructions**:
```bash
bash scripts/deploy.sh
python scripts/migrate.py
python scripts/verify.py
```

**Configuration**:
- Namespace: `database`
- Database: `mystery_skills`
- User: `mystery_skills_user`
- Password: Auto-generated (stored in Secret)

**Expected Output**: `✓ PostgreSQL deployed | ✓ 8 migrations applied | ✓ Connection verified`

**Token Cost**: ~105 tokens

---

#### Skill 4: dapr-setup

**File**: `.claude/skills/dapr-setup/SKILL.md`

**Purpose**: Configure Dapr components for pub/sub, state, and secrets

**When to Use**:
- Setting up event-driven architecture
- Need state management across microservices
- Integrating with Kafka and PostgreSQL via Dapr

**What It Does**:
1. Installs Dapr runtime to Kubernetes
2. Creates Dapr components:
   - `kafka-pubsub.yaml` (pub/sub component for Kafka)
   - `postgres-state.yaml` (state store component for PostgreSQL)
   - `kubernetes-secrets.yaml` (secret store component)
3. Verifies Dapr control plane is running

**Instructions**:
```bash
bash scripts/install_dapr.sh
kubectl apply -f components/
python scripts/verify.py
```

**Expected Output**: `✓ Dapr installed | ✓ 3 components configured | ✓ Control plane healthy`

**Token Cost**: ~95 tokens

---

#### Skill 5: fastapi-dapr-agent

**File**: `.claude/skills/fastapi-dapr-agent/SKILL.md`

**Purpose**: Create FastAPI microservice with Dapr sidecar integration

**When to Use**:
- Creating Mystery Skills AI agent services
- Building event-driven microservices
- Need pub/sub, state management, or service invocation

**What It Does**:
1. Scaffolds FastAPI project with Dapr
2. Configures pub/sub for Kafka
3. Sets up state store (PostgreSQL via Dapr)
4. Creates Kubernetes manifests with Dapr annotations
5. Includes health checks and observability

**Instructions**:
```bash
python scripts/scaffold_service.py --name triage-agent --port 8001
bash scripts/build.sh triage-agent
bash scripts/deploy.sh triage-agent
```

**Service Structure**:
```
backend/<service-name>/
├── main.py                 # FastAPI app
├── agents/
│   └── agent.py           # AI agent logic
├── models/
│   └── schemas.py         # Pydantic models
├── dapr/
│   ├── pubsub.yaml        # Pub/Sub component
│   └── statestore.yaml    # State store component
├── k8s/
│   ├── deployment.yaml    # K8s deployment with Dapr
│   └── service.yaml       # K8s service
├── Dockerfile
└── requirements.txt
```

**Expected Output**: `✓ Service scaffolded | ✓ Docker image built | ✓ Deployed to K8s | ✓ Health check passed`

**Token Cost**: ~120 tokens

---

#### Skill 6: nextjs-k8s-deploy

**File**: `.claude/skills/nextjs-k8s-deploy/SKILL.md`

**Purpose**: Deploy Next.js application to Kubernetes

**When to Use**:
- Deploying Mystery Skills frontend
- Need production-ready Next.js deployment
- Want Kubernetes-native frontend hosting

**What It Does**:
1. Builds Next.js production bundle
2. Creates optimized Docker image
3. Generates Kubernetes manifests (Deployment + Service + Ingress)
4. Deploys to cluster
5. Configures environment variables

**Instructions**:
```bash
bash scripts/build.sh
bash scripts/deploy.sh --namespace mystery-skills
python scripts/verify.py
```

**Expected Output**: `✓ Next.js built | ✓ Image pushed | ✓ Deployed to K8s | ✓ Ingress configured`

**Token Cost**: ~115 tokens

---

#### Skill 7: mcp-code-execution

**File**: `.claude/skills/mcp-code-execution/SKILL.md`

**Purpose**: MCP server integration with code execution pattern for token efficiency

**When to Use**:
- Need to access external data/APIs from agents
- Want to reduce context bloat from MCP responses
- Implementing infrastructure monitoring

**What It Does**:
1. Wraps MCP server calls in code execution scripts
2. Filters and summarizes data client-side (0 tokens in context)
3. Returns minimal, decision-ready output (~10 tokens)

**Example**:
```python
# scripts/get_cluster_health.py
from mcp_kubernetes import KubernetesClient

client = KubernetesClient()
pods = client.get_pods(namespace="mystery-skills")

# Filter CLIENT-SIDE (0 tokens in agent context)
healthy = sum(1 for p in pods if p.status.phase == "Running")
total = len(pods)

# Return MINIMAL output
if healthy == total:
    print(f"✓ All {total} services healthy")
else:
    print(f"✗ {healthy}/{total} healthy")
```

**Expected Output**: `✓ All 6 services healthy` (~10 tokens vs 25,000 raw)

**Token Cost**: ~95 tokens

---

## Phase 3: Agents Required

### Agent Inventory

| # | Agent Name | Purpose | Port | Tech Stack | Priority | Status |
|---|------------|---------|------|------------|----------|--------|
| 1 | Triage Agent | Route queries to specialists | 8001 | FastAPI + Claude API | CRITICAL | 📋 Planned |
| 2 | Concepts Agent | Explain Python concepts | 8002 | FastAPI + Claude API | CRITICAL | 📋 Planned |
| 3 | Code Review Agent | Analyze code quality | 8003 | FastAPI + Claude API | HIGH | 📋 Planned |
| 4 | Debug Agent | Help debug errors | 8004 | FastAPI + Claude API | HIGH | 📋 Planned |
| 5 | Exercise Agent | Generate/grade exercises | 8005 | FastAPI + Claude API | MEDIUM | 📋 Planned |
| 6 | Progress Agent | Track learning progress | 8006 | FastAPI + PostgreSQL | MEDIUM | 📋 Planned |

### Agent Specifications

#### Agent 1: Triage Agent

**Port**: 8001
**Namespace**: mystery-skills

**Purpose**: Route student queries to specialized agents based on intent classification

**Input**:
- User ID
- Query text
- Conversation context (optional)

**Output**:
- Target agent (concepts | debug | code_review | exercise | progress)
- Confidence score (0.0-1.0)
- Routing reason

**Behavior**:
1. Analyze query using Claude API
2. Classify intent using few-shot prompting
3. If confidence < 0.7, route to Concepts (safest default)
4. Publish routing decision to Kafka topic: `query.routed`
5. Return immediately (async processing)

**Non-Functional Requirements**:
- Latency: <500ms p95
- Availability: 99.9%
- Rate limit: 100 req/sec per student

**Dependencies**:
- Kafka topic: `query.received` (subscribe)
- Kafka topic: `query.routed` (publish)
- PostgreSQL: `query_history` table
- Claude API: classification model

**Dapr Integration**:
- Pub/Sub: `kafka-pubsub`
- State Store: `postgres-state`

**Validation**:
- Health check: `GET /health`
- Metrics: `GET /metrics`
- Test classification: `POST /test`

---

#### Agent 2: Concepts Agent

**Port**: 8002
**Namespace**: mystery-skills

**Purpose**: Explain Python concepts with examples, adapted to student skill level

**Input**:
- User ID
- Topic/concept name
- Student skill level (beginner | learning | proficient | mastered)
- Context (current module, mastery score)

**Output**:
- Personalized explanation
- Code examples
- Visualization suggestions
- Related topics

**Behavior**:
1. Receive query from Kafka topic: `query.routed` (filter: agent='concepts')
2. Fetch student skill level from PostgreSQL
3. Generate explanation using Claude API with context
4. Optionally offer quiz
5. Publish response to Kafka topic: `response.ready`

**Claude API Integration**:
- Model: Claude Sonnet 4.5
- System Prompt: "You are a patient Python tutor. Adapt explanations to {skill_level}."
- Max Tokens: 1500
- Temperature: 0.7

**Non-Functional Requirements**:
- Latency: <2s p95 (includes Claude API call)
- Availability: 99.5%
- Cache frequent concepts (Redis optional)

**Dependencies**:
- Kafka topics: `query.routed`, `response.ready`
- PostgreSQL: `student_profiles`, `module_progress`
- Claude API

---

#### Agent 3: Code Review Agent

**Port**: 8003
**Namespace**: mystery-skills

**Purpose**: Analyze code for correctness, style (PEP 8), efficiency, readability

**Input**:
- User ID
- Code snippet
- Module context

**Output**:
- Correctness score (0.0-1.0)
- Style issues (PEP 8 violations)
- Efficiency score
- Readability score
- Overall score (weighted average)
- Suggestions for improvement

**Behavior**:
1. Parse code using Python AST
2. Run static analysis (pylint, flake8)
3. Use Claude API for semantic review
4. Calculate weighted score:
   - Correctness: 40%
   - Style: 30%
   - Efficiency: 20%
   - Readability: 10%
5. Update `code_quality` in `module_progress` table
6. Return feedback

**Non-Functional Requirements**:
- Latency: <3s p95
- Availability: 99.5%
- Handle code up to 500 lines

**Dependencies**:
- PostgreSQL: `module_progress`
- Claude API (for semantic analysis)
- Python AST parser

---

#### Agent 4: Debug Agent

**Port**: 8004
**Namespace**: mystery-skills

**Purpose**: Parse errors, identify root causes, provide hints before solutions

**Input**:
- User ID
- Code snippet
- Error message
- Error type
- Attempt number

**Output**:
- Error type classification
- Root cause analysis
- Hint (without giving away solution)
- Full solution (if requested)
- Explanation

**Behavior**:
1. Receive error from Kafka topic
2. Parse error traceback
3. Identify error pattern (syntax, name, type, etc.)
4. Check if same error type occurred 3+ times → trigger struggle alert
5. Use Claude API to generate hint
6. Return incremental help (hint first, solution only if stuck)

**Struggle Detection**:
- Same error type 3+ times → Alert
- Record in `struggle_alerts` table
- Publish to `struggle.detected` Kafka topic

**Non-Functional Requirements**:
- Latency: <2s p95
- Availability: 99.5%

**Dependencies**:
- Kafka topics: `query.routed`, `struggle.detected`
- PostgreSQL: `code_executions`, `struggle_alerts`
- Claude API

---

#### Agent 5: Exercise Agent

**Port**: 8005
**Namespace**: mystery-skills

**Purpose**: Generate and auto-grade coding challenges

**Input (Generate)**:
- Teacher ID
- Module name
- Topic
- Difficulty level
- Count

**Output (Generate)**:
- Array of exercises with:
  - Title
  - Description
  - Starter code
  - Test cases

**Input (Submit)**:
- Student ID
- Exercise ID
- Submitted code

**Output (Submit)**:
- Passed (boolean)
- Tests passed / total
- Score (0-100)
- Feedback from Code Review Agent

**Behavior**:
1. Generate exercise using Claude API (teacher request)
2. Store in `exercises` table
3. On submission:
   - Run code in sandbox (RestrictedPython + Docker)
   - Execute test cases
   - Calculate score
   - Request code review
4. Update `exercise_completion` in `module_progress`

**Non-Functional Requirements**:
- Latency: <5s p95 (includes code execution)
- Sandbox timeout: 5s
- Memory limit: 50MB

**Dependencies**:
- PostgreSQL: `exercises`, `exercise_submissions`, `module_progress`
- Code sandbox (Docker container with RestrictedPython)
- Code Review Agent (service invocation via Dapr)
- Claude API (for exercise generation)

---

#### Agent 6: Progress Agent

**Port**: 8006
**Namespace**: mystery-skills

**Purpose**: Track mastery scores and provide progress summaries

**Input**:
- Student ID
- Timeframe (optional)

**Output**:
- Overall mastery score
- Module-by-module breakdown
- Mastery levels (beginner | learning | proficient | mastered)
- Color codes (red | yellow | green | blue)
- Streak days
- Recent activity

**Behavior**:
1. Query PostgreSQL for student data
2. Calculate mastery scores using weighted formula:
   - Exercise completion: 40%
   - Quiz scores: 30%
   - Code quality ratings: 20%
   - Consistency (streak): 10%
3. Determine mastery level:
   - 0-40% → Beginner (Red)
   - 41-70% → Learning (Yellow)
   - 71-90% → Proficient (Green)
   - 91-100% → Mastered (Blue)
4. Return comprehensive progress report

**Non-Functional Requirements**:
- Latency: <500ms p95 (database query only)
- Availability: 99.9%
- Cache for 5 minutes (Redis optional)

**Dependencies**:
- PostgreSQL: `student_profiles`, `module_progress`, `query_history`, `code_executions`, `exercise_submissions`

---

## Phase 4: UI Customization Plan

### Current UI Analysis

**Existing Features** (from flash-ui-1):
- ✅ Deep dark theme (#09090b)
- ✅ Glassmorphism with backdrop blur
- ✅ 3D perspective (1500px)
- ✅ Card grid layout
- ✅ Floating input with animations
- ✅ Focus mode
- ✅ Side drawer
- ✅ Code streaming preview
- ✅ Mobile responsive
- ✅ React 19 + TypeScript

**Required Modifications**:

### Modification 1: Rebrand to Mystery Skills

**Files to Edit**:
- `frontend/learnflow-ui/index.html` (title, meta)
- `frontend/learnflow-ui/index.tsx` (app title)
- `frontend/learnflow-ui/index.css` (keep dark theme)

**Changes**:
```typescript
// Before
<title>Diffusion Chat</title>

// After
<title>Mystery Skills - The Learning Revolution</title>
```

### Modification 2: Add Terminal/Hacker Aesthetic

**New Component**: `frontend/learnflow-ui/components/TerminalChat.tsx`

**Features**:
- Terminal-style prompt: `maya@mystery-skills:~/python/loops$`
- JetBrains Mono font
- Matrix rain effect background (optional)
- Scanline overlay
- Glitch hover effects on buttons
- Agent avatar with neon glow

**CSS Variables to Add**:
```css
--terminal-green: #00FF41; /* Matrix green */
--terminal-blue: #00BFFF;  /* Logic blue */
--terminal-red: #FF4444;   /* Cyber alert red */
--font-mono: 'JetBrains Mono', 'Roboto Mono', monospace;
```

### Modification 3: Add 3D Mastery Sphere

**New Component**: `frontend/learnflow-ui/components/MasterySphere.tsx`

**Technology**: React Three Fiber (Three.js wrapper for React)

**Features**:
- 8 orbital rings (one per Python module)
- Color-coded based on mastery:
  - Red (0-40%): Beginner
  - Yellow (41-70%): Learning
  - Green (71-90%): Proficient
  - Blue (91-100%): Mastered
- Center percentage display (holographic effect)
- Rotation on mouse movement
- Pulse effect when mastery level changes
- Amber pulse for struggle detection

**Props**:
```typescript
interface MasterySphereProps {
  modules: Array<{
    name: string;
    mastery: number; // 0-100
  }>;
  overallMastery: number;
  isStruggling?: boolean;
}
```

### Modification 4: Add Agent Visualization

**New Component**: `frontend/learnflow-ui/components/AgentBridge.tsx`

**Features**:
- 6 agent avatars (Triage, Concepts, Debug, Code Review, Exercise, Progress)
- Active agent glow effect
- Routing animation (data packets flowing from Triage to target)
- Agent status indicator (idle | thinking | responding)
- Real-time "thinking" logs (JSON metadata scroll)

**Routing Animation**:
```typescript
// Triage -> Concepts
<motion.div
  initial={{ x: 0, opacity: 0 }}
  animate={{ x: 200, opacity: 1 }}
  transition={{ duration: 0.5 }}
  className="routing-packet"
/>
```

### Modification 5: Add Monaco Editor

**Package**: `@monaco-editor/react`

**New Component**: `frontend/learnflow-ui/components/CodeEditor.tsx`

**Features**:
- Python syntax highlighting
- Dark theme (vs-dark)
- "Run in Sandbox" button
- Real-time output panel
- Error highlighting
- Line numbers
- Auto-completion

**Integration**:
```typescript
import Editor from '@monaco-editor/react';

<Editor
  height="400px"
  defaultLanguage="python"
  theme="vs-dark"
  value={code}
  onChange={setCode}
  options={{
    minimap: { enabled: false },
    fontSize: 14,
  }}
/>
```

### Modification 6: Add Infrastructure HUD

**New Component**: `frontend/learnflow-ui/components/InfrastructureHUD.tsx`

**Features**:
- Live Kafka topic ticker (scrolling)
- Dapr sidecar status indicators
- Skill Vault (MCP skills list)
- "Deploy to K8s" buttons for each skill
- Real-time health pings from Minikube
- Token efficiency counter

**Layout** (Bento Grid):
```
┌─────────────┬─────────────┐
│   Kafka     │   Dapr      │
│   Topics    │   Status    │
├─────────────┴─────────────┤
│   Skill Vault              │
│   - kafka-k8s-setup [✓]    │
│   - postgres-k8s-setup [✓] │
│   - dapr-setup [✓]         │
└────────────────────────────┘
```

### Modification 7: Add Teacher Struggle Alert

**New Component**: `frontend/learnflow-ui/components/StruggleAlert.tsx`

**Features**:
- Amber glow when triggered
- Student name and struggle type
- Context (e.g., "5 failed executions on list comprehensions")
- "Generate Exercise" button (one-click)
- "View Code Attempts" button
- Dismiss button

**Trigger Types**:
- Same error 3+ times
- Stuck on exercise >10 min
- Quiz score <50%
- Student says "I don't understand"
- 5+ failed executions

---

## Phase 5: Development Roadmap

### Sprint Plan (8 Days)

#### Day 1: Foundation Setup ✅

**Completed**:
- ✅ Constitution created
- ✅ Project structure established
- ✅ UI copied to frontend directory
- ✅ GitHub repository configured
- ✅ README documentation
- ✅ PHR for setup session

**Remaining** (2 hours):
- ⏳ Commit to GitHub
- ⏳ Create feature branch for infrastructure

---

#### Day 2: Infrastructure Skills (8 hours)

**Morning** (4 hours):
1. Create `agents-md-gen` skill (1 hour)
   - Write SKILL.md
   - Create scripts (analyze, generate, validate)
   - Test on reusable_intelligence repo
   - Validate with Claude Code + Goose

2. Create `kafka-k8s-setup` skill (1.5 hours)
   - Write SKILL.md and REFERENCE.md
   - Create deploy.sh (Helm install)
   - Create verify.py (pod status check)
   - Create create_test_topic.sh
   - Test deployment to Minikube

3. Create `postgres-k8s-setup` skill (1.5 hours)
   - Write SKILL.md
   - Create deploy.sh
   - Create migrate.py (schema migrations)
   - Create verify.py (connection test)

**Afternoon** (4 hours):
4. Create `dapr-setup` skill (2 hours)
   - Write SKILL.md
   - Create install_dapr.sh
   - Create Dapr components:
     - kafka-pubsub.yaml
     - postgres-state.yaml
     - kubernetes-secrets.yaml
   - Create verify.py
   - Test Dapr control plane

5. Test single-prompt deployment (2 hours)
   - Deploy all infrastructure with one prompt
   - Measure token usage
   - Validate 99%+ reduction claim
   - Document results

**Success Criteria**:
- ✅ All 4 skills working
- ✅ Tested on Claude Code AND Goose
- ✅ Token budget <350 tokens
- ✅ Kafka + PostgreSQL + Dapr running in Minikube

**Commit**: `feat(skills): Infrastructure skills - Kafka, PostgreSQL, Dapr`

---

#### Day 3: Application Skills (8 hours)

**Morning** (4 hours):
1. Create `fastapi-dapr-agent` skill (4 hours)
   - Write SKILL.md and REFERENCE.md
   - Create scaffold_service.py
   - Create build.sh
   - Create deploy.sh
   - Test by creating Triage Agent
   - Validate Dapr annotations work

**Afternoon** (4 hours):
2. Build Triage Agent (2 hours)
   - Use `fastapi-dapr-agent` skill
   - Implement query routing logic
   - Integrate Claude API
   - Test Kafka pub/sub

3. Build Concepts Agent (2 hours)
   - Use `fastapi-dapr-agent` skill
   - Implement explanation generation
   - Integrate Claude API with context
   - Test skill level adaptation

**Success Criteria**:
- ✅ `fastapi-dapr-agent` skill complete
- ✅ Triage Agent routing correctly
- ✅ Concepts Agent generating explanations
- ✅ Both deployed to Minikube

**Commit**: `feat(skills): FastAPI-Dapr skill and first 2 agents`

---

#### Day 4: Remaining Agents (8 hours)

**Morning** (4 hours):
1. Build Code Review Agent (2 hours)
   - Use `fastapi-dapr-agent` skill
   - Implement AST parsing
   - Integrate pylint/flake8
   - Use Claude API for semantic review

2. Build Debug Agent (2 hours)
   - Use `fastapi-dapr-agent` skill
   - Implement error parsing
   - Implement struggle detection
   - Integrate Claude API for hints

**Afternoon** (4 hours):
3. Build Exercise Agent (2 hours)
   - Use `fastapi-dapr-agent` skill
   - Implement exercise generation
   - Implement code sandbox (Docker + RestrictedPython)
   - Test auto-grading

4. Build Progress Agent (2 hours)
   - Use `fastapi-dapr-agent` skill
   - Implement mastery calculation
   - Query optimization
   - Test score updates

**Success Criteria**:
- ✅ All 6 agents deployed
- ✅ End-to-end flow working (Maya scenario)
- ✅ Struggle detection working (James scenario)

**Commit**: `feat(agents): All 6 AI agents operational`

---

#### Day 5: Frontend Customization (8 hours)

**Morning** (4 hours):
1. Rebrand to Mystery Skills (1 hour)
   - Update titles, branding
   - Add "by Syeda Alishba Fatima"
   - Update colors (keep dark theme)

2. Add Terminal/Hacker Aesthetic (3 hours)
   - Create TerminalChat component
   - Add JetBrains Mono font
   - Add glitch effects
   - Add scanline overlay
   - Test agent interactions

**Afternoon** (4 hours):
3. Add 3D Mastery Sphere (2 hours)
   - Install React Three Fiber
   - Create MasterySphere component
   - Implement 8 orbital rings
   - Add color coding
   - Test animations

4. Add Monaco Editor (2 hours)
   - Install @monaco-editor/react
   - Create CodeEditor component
   - Add "Run in Sandbox" button
   - Test Python syntax highlighting

**Success Criteria**:
- ✅ UI fully rebranded
- ✅ Terminal aesthetic working
- ✅ 3D sphere rendering
- ✅ Code editor functional

**Commit**: `feat(ui): Mystery Skills rebrand with terminal aesthetic and 3D sphere`

---

#### Day 6: Integration & Testing (8 hours)

**Morning** (4 hours):
1. Connect UI to Backend (3 hours)
   - Replace Google GenAI with FastAPI endpoints
   - Implement Better Auth
   - Connect to Kafka topics
   - Test agent communication

2. Add Infrastructure HUD (1 hour)
   - Create InfrastructureHUD component
   - Connect to health endpoints
   - Test real-time updates

**Afternoon** (4 hours):
3. Add Teacher Features (2 hours)
   - Create StruggleAlert component
   - Implement teacher dashboard
   - Test struggle detection
   - Test exercise generation

4. End-to-End Testing (2 hours)
   - Test Maya scenario (student flow)
   - Test James scenario (struggle detection)
   - Test teacher flow (Mr. Rodriguez)
   - Fix bugs

**Success Criteria**:
- ✅ Full integration working
- ✅ All 3 scenarios passing
- ✅ No critical bugs

**Commit**: `feat(integration): Full-stack integration and teacher features`

---

#### Day 7: CI/CD & Cloud Deployment (8 hours)

**Morning** (4 hours):
1. Create `nextjs-k8s-deploy` skill (2 hours)
   - Write SKILL.md
   - Create build.sh
   - Create deploy.sh
   - Test frontend deployment

2. Setup GitHub Actions (2 hours)
   - Create `.github/workflows/ci.yml`
   - Add tests for each agent
   - Add Docker build steps
   - Test CI pipeline

**Afternoon** (4 hours):
3. Setup ArgoCD (2 hours)
   - Install ArgoCD to Minikube
   - Create ArgoCD application manifests
   - Configure GitOps sync
   - Test auto-deployment

4. Cloud Deployment (2 hours)
   - Choose cloud provider (Azure/GCP/Oracle)
   - Deploy to cloud K8s cluster
   - Configure DNS and SSL
   - Test production deployment

**Success Criteria**:
- ✅ CI pipeline working
- ✅ ArgoCD deploying automatically
- ✅ Production deployment live

**Commit**: `feat(cicd): GitHub Actions + ArgoCD GitOps deployment`

---

#### Day 8: Documentation & Demo (6 hours)

**Morning** (3 hours):
1. Create Docusaurus Site (1.5 hours)
   - Install Docusaurus
   - Create documentation structure
   - Add architecture diagrams
   - Document API endpoints

2. Generate AGENTS.md (0.5 hour)
   - Use `agents-md-gen` skill
   - Validate completeness

3. Create ADRs (1 hour)
   - Document key architectural decisions
   - Format: Why Dapr? Why FastAPI? Why Event-Driven?

**Afternoon** (3 hours):
4. Create Demo Video (2 hours)
   - Record Maya scenario
   - Record James scenario (struggle detection)
   - Record teacher dashboard
   - Show infrastructure HUD
   - Show token efficiency

5. Final Polish (1 hour)
   - Fix any remaining bugs
   - Update README
   - Prepare submission

**Success Criteria**:
- ✅ Comprehensive documentation
- ✅ Professional demo video
- ✅ All ADRs created
- ✅ Ready to submit

**Commit**: `docs: Complete documentation and demo preparation`

---

## Phase 6: Validation & Acceptance

### Acceptance Criteria

**Skills Autonomy (15/15)**:
- ✅ Single prompt deploys entire infrastructure
- ✅ Single prompt creates each agent service
- ✅ Zero manual intervention required
- ✅ Skills work identically on Claude Code and Goose

**Token Efficiency (10/10)**:
- ✅ Total deployment <780 tokens
- ✅ 99.3% reduction vs traditional MCP (115,000 tokens)
- ✅ Validation scripts return ~10 tokens (not 5000)
- ✅ MCP Code Execution pattern implemented

**Cross-Agent Compatibility (5/5)**:
- ✅ All skills tested on Claude Code
- ✅ All skills tested on Goose
- ✅ Identical results on both agents
- ✅ AAIF-compliant skill structure

**Architecture (18/20)**:
- ✅ Kafka pub/sub for agent communication
- ✅ Dapr sidecars for state/secrets/invocation
- ✅ Stateless microservices
- ✅ PostgreSQL state store
- ✅ Event-driven patterns
- ✅ Kubernetes orchestration
- ⚠️ (May lose 2 points for complexity)

**MCP Integration (10/10)**:
- ✅ MCP Code Execution pattern implemented
- ✅ Token efficiency demonstrated
- ✅ Scripts return decision-ready summaries
- ✅ No context bloat

**Documentation (10/10)**:
- ✅ Comprehensive Docusaurus site
- ✅ AGENTS.md auto-generated
- ✅ ADRs for architectural decisions
- ✅ API documentation (OpenAPI)

**Spec-Kit Plus Usage (15/15)**:
- ✅ Spec-driven development (this plan.md)
- ✅ Specs translate to agentic instructions
- ✅ Constitution guides all decisions
- ✅ PHRs for every major decision

**LearnFlow Completion (15/15)**:
- ✅ All 6 agents operational
- ✅ UI fully functional
- ✅ Maya scenario working
- ✅ James scenario working (struggle detection)
- ✅ Teacher dashboard working
- ✅ Built entirely via skills

**Total Score Target**: 85-98/100 (Top Tier)

---

## Risk Assessment

### High-Impact Risks

**Risk 1: Token Quota Exhaustion**
- **Probability**: Medium
- **Impact**: High (can't complete hackathon)
- **Mitigation**:
  - Monitor token usage daily
  - Use Code Execution pattern religiously
  - Cache agent responses where possible
  - Use Haiku model for simple tasks

**Risk 2: Claude API Rate Limits**
- **Probability**: Medium
- **Impact**: High (agents can't respond)
- **Mitigation**:
  - Implement exponential backoff
  - Queue requests when near limit
  - Use multiple API keys if allowed
  - Implement rate limiting on frontend

**Risk 3: Kafka Message Loss**
- **Probability**: Low
- **Impact**: Medium (lost queries)
- **Mitigation**:
  - Persistent Kafka topics
  - Consumer groups with offset management
  - Retry logic in agents
  - Message acknowledgment

**Risk 4: Database Bottleneck**
- **Probability**: Medium
- **Impact**: Medium (slow responses)
- **Mitigation**:
  - Connection pooling (SQLAlchemy)
  - Database indexes on frequently queried fields
  - Optional: Redis caching layer
  - Read replicas if needed

**Risk 5: Code Sandbox Security**
- **Probability**: Low
- **Impact**: Critical (arbitrary code execution)
- **Mitigation**:
  - RestrictedPython for Python execution
  - Docker container isolation
  - 5s timeout
  - 50MB memory limit
  - No file system access (except temp)
  - No network access

**Risk 6: Integration Testing Complexity**
- **Probability**: High
- **Impact**: Medium (delays)
- **Mitigation**:
  - Test each agent independently first
  - Use contract testing
  - Mock Kafka for unit tests
  - Dedicated integration testing day (Day 6)

---

## Next Steps (Immediate)

### Today (Day 1 - Remaining 2 hours)

**Step 1: Commit Current Progress**
```bash
git add .
git commit -m "feat: Complete planning phase

- Implementation plan created (specs/mystery-skills-platform/plan.md)
- Architecture defined (event-driven microservices)
- 7 skills identified (780 token budget)
- 6 agents specified (Triage, Concepts, Debug, Review, Exercise, Progress)
- UI customization plan (terminal aesthetic + 3D sphere)
- 8-day development roadmap
- Risk assessment and mitigation strategies

🤖 Generated with Claude Code
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

git push origin master
```

**Step 2: Create Feature Branch for Infrastructure**
```bash
git checkout -b 001-infrastructure-skills
```

**Step 3: Create PHR for Planning Session**
```bash
# Will be automated via sp.phr workflow
```

---

### Tomorrow (Day 2 - 8 hours)

**Priority 1: Create Infrastructure Skills**
1. `agents-md-gen` skill (1 hour)
2. `kafka-k8s-setup` skill (1.5 hours)
3. `postgres-k8s-setup` skill (1.5 hours)
4. `dapr-setup` skill (2 hours)

**Priority 2: Test Single-Prompt Deployment**
- Deploy entire infrastructure with one command
- Measure actual token usage
- Validate 99%+ reduction

**Priority 3: Cross-Agent Validation**
- Test all skills on Claude Code
- Test all skills on Goose
- Document any differences

---

## Appendix

### Python Curriculum Modules

1. **Basics**: Variables, Data Types, Input/Output, Operators, Type Conversion
2. **Control Flow**: Conditionals (if/elif/else), For Loops, While Loops, Break/Continue
3. **Data Structures**: Lists, Tuples, Dictionaries, Sets
4. **Functions**: Defining Functions, Parameters, Return Values, Scope
5. **OOP**: Classes & Objects, Attributes & Methods, Inheritance, Encapsulation
6. **Files**: Reading/Writing Files, CSV Processing, JSON Handling
7. **Errors**: Try/Except, Exception Types, Custom Exceptions, Debugging
8. **Libraries**: Installing Packages, Working with APIs, Virtual Environments

### Mastery Level Calculation

**Formula**:
```
Mastery Score = (Exercise Completion × 0.40) +
                (Quiz Scores × 0.30) +
                (Code Quality × 0.20) +
                (Consistency/Streak × 0.10)
```

**Levels**:
- 0-40%: Beginner (Red)
- 41-70%: Learning (Yellow)
- 71-90%: Proficient (Green)
- 91-100%: Mastered (Blue)

### Struggle Detection Triggers

1. Same error type 3+ times
2. Stuck on exercise >10 minutes
3. Quiz score <50%
4. Student says "I don't understand" or "I'm stuck"
5. 5+ failed code executions in a row

---

**End of Implementation Plan**

**Status**: Phase 0 Complete - Ready for Day 2 Execution
**Next Milestone**: Infrastructure Skills Operational
**Target Date**: 2025-12-30 (Tomorrow)
