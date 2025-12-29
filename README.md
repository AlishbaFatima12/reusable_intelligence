# LearnFlow - AI-Powered Learning Platform
## Hackathon III: Reusable Intelligence & Cloud-Native Mastery

**Repository**: [reusable_intelligence](https://github.com/AlishbaFatima12/reusable_intelligence)
**Team**: AlishbaFatima12
**Last Updated**: 2025-12-29

---

## Project Overview

LearnFlow is an **AI-native learning platform** that uses specialized AI agents to provide personalized programming education. Built using **agent-native development principles**, LearnFlow demonstrates the power of reusable intelligence through skills-based architecture.

### The LearnFlow Difference

- **6 Specialized AI Agents**: Triage, Concepts, Code Review, Debug, Exercise, and Progress
- **Real-time Collaboration**: Agents communicate via Kafka event streaming
- **Personalized Learning**: Each student gets AI tutoring adapted to their skill level
- **Cloud-Native**: Built for scale with Kubernetes, Dapr, and microservices

---

## Architecture

### High-Level Architecture

```
Student Query → API Gateway → Kafka: query.received
                                      ↓
                                Triage Agent (AI classification)
                                      ↓
                                Kafka: query.routed
                      ┌───────────────┴────────────────┐
                      ↓                                ↓
            Concepts Agent (AI)              Debug Agent (AI)
            Code Review Agent (AI)           Exercise Agent (AI)
            Progress Agent (Analytics)
                      ↓
            Kafka: response.ready
                      ↓
            API Gateway → Student (Next.js UI)
```

### Technology Stack

**Frontend**:
- Next.js + React 19 + TypeScript
- Monaco Editor (code editing)
- Immersive dark UI with glassmorphism

**Backend**:
- FastAPI (Python 3.11+) microservices
- Dapr sidecar (pub/sub, state, service invocation)
- Apache Kafka (event streaming)
- PostgreSQL (state persistence)

**AI/ML**:
- Claude API (Anthropic) for AI agent intelligence
- Vector database for learned explanations
- Context-aware personalization

**Infrastructure**:
- Kubernetes (orchestration)
- Docker (containerization)
- ArgoCD (GitOps CD)
- GitHub Actions (CI)

**Observability**:
- Structured JSON logging
- Prometheus metrics
- Jaeger/Zipkin tracing (via Dapr)

---

## Project Structure

```
reusable_intelligence/
├── .claude/                    # Claude Code skills
│   └── skills/
│       ├── agents-md-gen/      # Generate AGENTS.md
│       ├── kafka-k8s-setup/    # Deploy Kafka
│       ├── postgres-k8s-setup/ # Deploy PostgreSQL
│       ├── fastapi-dapr-agent/ # Create microservices
│       ├── nextjs-k8s-deploy/  # Deploy frontend
│       └── mcp-code-execution/ # MCP integration
├── backend/                    # Microservices
│   ├── triage-agent/          # Query routing (AI)
│   ├── concepts-agent/        # Concept explanations (AI)
│   ├── debug-agent/           # Code debugging (AI)
│   ├── code-review-agent/     # Code review (AI)
│   ├── exercise-agent/        # Exercise generation (AI)
│   └── progress-agent/        # Progress tracking
├── frontend/                   # Next.js application
│   └── learnflow-ui/          # Student & teacher dashboards
├── infrastructure/             # Kubernetes manifests
│   ├── kafka/                 # Kafka deployment
│   ├── postgres/              # PostgreSQL deployment
│   └── dapr/                  # Dapr components
├── specs/                      # Feature specifications
├── history/                    # Development history
│   ├── prompts/               # Prompt History Records (PHRs)
│   └── adr/                   # Architecture Decision Records
├── .specify/                   # SDD-RI artifacts
│   ├── memory/
│   │   └── constitution.md    # Project constitution
│   └── templates/             # Document templates
├── docs/                       # Documentation
└── README.md                  # This file
```

---

## Core Principles (Constitution)

### 1. Agent-Native Development
- AI agents are digital FTEs, not assistants
- Skills are the product; code is generated
- 168 hours/week autonomous work

### 2. Token Efficiency (98%+ Reduction)
- MCP Code Execution Pattern
- <1000 tokens for full deployment (vs 50,000+)
- Skills: ~100 tokens, Scripts: 0 tokens

### 3. Spec-Driven Development
- Specification precedes implementation
- Specs are executable blueprints
- Agents make autonomous decisions

### 4. Skills as Permanent Knowledge
- Reusable across projects and agents
- Cross-agent compatible (Claude Code + Goose)
- Composable with emergent capabilities

### 5. Event-Driven Cloud-Native
- Microservices via Kafka pub/sub
- Stateless services + Dapr state management
- Kubernetes for scale and resilience

Read the full constitution: `.specify/memory/constitution.md`

---

## Getting Started

### Prerequisites

- **Docker** (24.0+)
- **Minikube** (1.32+)
- **Helm** (3.13+)
- **Claude Code** or **Goose** (agent runtime)
- **Node.js** (20+)
- **Python** (3.11+)

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AlishbaFatima12/reusable_intelligence.git
   cd reusable_intelligence
   ```

2. **Start Minikube**:
   ```bash
   minikube start --cpus=4 --memory=8192 --driver=docker
   ```

3. **Deploy infrastructure** (using skills):
   ```bash
   # With Claude Code
   claude "Deploy Kafka to Kubernetes using kafka-k8s-setup skill"
   claude "Deploy PostgreSQL using postgres-k8s-setup skill"

   # Or with Goose
   goose run "Deploy Kafka and PostgreSQL infrastructure"
   ```

4. **Build LearnFlow agents** (autonomous):
   ```bash
   claude "Build all 6 LearnFlow microservices from specifications"
   ```

5. **Deploy frontend**:
   ```bash
   claude "Deploy LearnFlow UI using nextjs-k8s-deploy skill"
   ```

6. **Verify deployment**:
   ```bash
   kubectl get pods -A
   # All pods should be Running
   ```

7. **Access LearnFlow**:
   ```bash
   minikube service learnflow-frontend -n learnflow
   ```

### Development Workflow

1. **Create specification**: Define feature in `specs/<feature>/spec.md`
2. **Create/use skill**: Build reusable skill or use existing
3. **Autonomous build**: Agent implements from spec + skill
4. **Validate**: Automated validation scripts verify success
5. **Deploy**: GitOps via ArgoCD (auto-deployment from main branch)

---

## Skills Library

### Infrastructure Skills

| Skill | Purpose | Token Cost | Status |
|-------|---------|------------|--------|
| `kafka-k8s-setup` | Deploy Kafka cluster | ~110 | ✅ Ready |
| `postgres-k8s-setup` | Deploy PostgreSQL DB | ~105 | ✅ Ready |
| `dapr-setup` | Configure Dapr components | ~95 | 🚧 In Progress |

### Application Skills

| Skill | Purpose | Token Cost | Status |
|-------|---------|------------|--------|
| `fastapi-dapr-agent` | Create FastAPI microservice | ~120 | ✅ Ready |
| `nextjs-k8s-deploy` | Deploy Next.js app | ~115 | ✅ Ready |
| `mcp-code-execution` | MCP with code execution | ~95 | 🚧 In Progress |

### Utility Skills

| Skill | Purpose | Token Cost | Status |
|-------|---------|------------|--------|
| `agents-md-gen` | Generate AGENTS.md | ~100 | ✅ Ready |
| `docusaurus-deploy` | Deploy documentation site | ~100 | 📋 Planned |

**Total Token Budget**: ~840 tokens (vs 115,000 traditional MCP) = **99.3% reduction**

---

## LearnFlow Agents

### 1. Triage Agent (AI)
- **Purpose**: Route student queries to specialized agents
- **Input**: User query text
- **Output**: Target agent + confidence score
- **AI Model**: Claude Sonnet 4.5 (classification)
- **Port**: 8001

### 2. Concepts Agent (AI)
- **Purpose**: Explain programming concepts
- **Input**: Concept name + student skill level
- **Output**: Personalized explanation
- **AI Model**: Claude Sonnet 4.5 (generation)
- **Port**: 8002

### 3. Code Review Agent (AI)
- **Purpose**: Review and improve student code
- **Input**: Code snippet + context
- **Output**: Review with suggestions
- **AI Model**: Claude Sonnet 4.5 (analysis)
- **Port**: 8003

### 4. Debug Agent (AI)
- **Purpose**: Help debug code errors
- **Input**: Code + error message
- **Output**: Debug strategy + fix
- **AI Model**: Claude Sonnet 4.5 (debugging)
- **Port**: 8004

### 5. Exercise Agent (AI)
- **Purpose**: Generate practice exercises
- **Input**: Topic + difficulty level
- **Output**: Coding exercise + test cases
- **AI Model**: Claude Sonnet 4.5 (generation)
- **Port**: 8005

### 6. Progress Agent (Analytics)
- **Purpose**: Track student learning progress
- **Input**: Student ID + timeframe
- **Output**: Progress metrics + insights
- **Data Source**: PostgreSQL state store
- **Port**: 8006

---

## UI Design

### Selected UI: "Diffusion Chat - Radical Redesign"

**Design Characteristics**:
- **Modern**: Deep dark theme (#09090b), glassmorphism, Inter font
- **Tech-Forward**: React 19, TypeScript, 3D perspective effects
- **Advanced**: Immersive full-screen, floating input, focus mode, code streaming

**Key Features**:
- Card-based artifact grid (perfect for multi-agent responses)
- Focus mode for detailed interactions
- Side drawer for code/variations
- Responsive mobile design
- Advanced animations (cubic-bezier, dramatic entrances)

**Location**: `frontend/learnflow-ui/`

**Modifications Needed**:
- Rebrand from "Diffusion Chat" → "LearnFlow"
- Adapt for educational context (learning queries, not UI generation)
- Add Monaco code editor integration
- Connect to FastAPI backend (replace Google GenAI)

---

## Token Efficiency Strategy

### MCP Code Execution Pattern

**Traditional MCP** (Avoid):
```
Agent → MCP Kubernetes → 15k tokens loaded
Agent → get_pods() → 5k tokens JSON returned
Agent → filter → 5k tokens processed
Total: 25k tokens
```

**Code Execution Pattern** (Use):
```python
# scripts/get_service_health.py
from mcp_kubernetes import KubernetesClient

client = KubernetesClient()
pods = client.get_pods(namespace="learnflow")

# Filter CLIENT-SIDE (0 tokens in agent context)
healthy = sum(1 for p in pods if p.status.phase == "Running")
total = len(pods)

# Return MINIMAL output
if healthy == total:
    print(f"✓ All {total} services healthy")
else:
    print(f"✗ {healthy}/{total} healthy")
```

**Agent sees**: `✓ All 6 services healthy` (~10 tokens)
**Reduction**: 99.96% (10 vs 25,000 tokens)

---

## Success Metrics

### Hackathon III Targets

| Criterion | Weight | Target | Status |
|-----------|--------|--------|--------|
| Skills Autonomy | 15% | Single-prompt deployment | 🚧 |
| Token Efficiency | 10% | 98%+ reduction | ✅ |
| Cross-Agent | 5% | Works on Claude + Goose | 📋 |
| Architecture | 20% | Event-driven, cloud-native | 🚧 |
| MCP Integration | 10% | Code execution pattern | 🚧 |
| Documentation | 10% | Auto-generated | 📋 |
| Spec-Kit Plus | 15% | Specs executable | 🚧 |
| LearnFlow | 15% | All 6 agents operational | 📋 |

**Target Score**: 85/100+ (Top Tier)

### Current Progress

- ✅ Constitution created
- ✅ UI selected and adapted
- ✅ GitHub repository configured
- ✅ Project structure established
- 🚧 Skills library (3/7 complete)
- 📋 Infrastructure deployment (planned)
- 📋 Agent implementation (planned)
- 📋 Integration testing (planned)

---

## Development Timeline

| Phase | Duration | Deliverable | Status |
|-------|----------|-------------|--------|
| **Setup** | Day 1 | Environment + foundation skills | ✅ |
| **Infrastructure** | Day 2 | Kafka + PostgreSQL deployed | 📋 |
| **Backend** | Day 3-4 | 6 AI agents operational | 📋 |
| **Frontend** | Day 5 | Next.js UI deployed | 📋 |
| **Integration** | Day 6 | End-to-end testing | 📋 |
| **Cloud Deploy** | Day 7 | ArgoCD + GitHub Actions | 📋 |
| **Polish** | Day 8 | Documentation + demo | 📋 |

---

## Contributing

This is a hackathon project. Contributions follow the constitution:

1. **Specification First**: Create `specs/<feature>/spec.md`
2. **Skills Over Code**: Build/use skills for implementation
3. **Validate Autonomously**: Include validation scripts
4. **Cross-Agent Test**: Verify on Claude Code AND Goose
5. **Token Efficient**: Measure and minimize token usage

---

## Resources

- **Constitution**: `.specify/memory/constitution.md`
- **Agent Principles**: `AGENT_NATIVE_PRINCIPLES.md`
- **Roadmap**: `HACKATHON_III_ROADMAP.md`
- **Prompt History**: `history/prompts/`
- **Architecture Decisions**: `history/adr/`

---

## License

MIT License - See LICENSE file

---

## Contact

**Team**: AlishbaFatima12
**Repository**: https://github.com/AlishbaFatima12/reusable_intelligence
**Hackathon**: Hackathon III - Reusable Intelligence & Cloud-Native Mastery

---

**Remember**: We're not building an app. We're building digital FTEs that build apps. Skills are the product; agents are the workforce.
