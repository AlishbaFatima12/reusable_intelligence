# LearnFlow Hackathon III Constitution
## Reusable Intelligence and Cloud-Native Mastery

## Core Principles

### I. Agent-Native Development (NON-NEGOTIABLE)
**AI agents are digital FTEs, not assistants**
- Skills are the product; code is generated
- Specs are executable blueprints readable by both humans and agents
- Intent-based instructions over step-by-step commands
- Agents build AND operate the system (build-time + runtime autonomy)
- 168 hours/week autonomous work, 99%+ consistency, instant scaling

**Implementation Requirements:**
- Every feature starts with a specification
- Skills must be composable and cross-agent compatible (Claude Code + Goose + future agents)
- Validation scripts must return minimal, parseable output (~10 tokens, not 5000)
- Single-prompt deployment required (no manual intervention)

### II. Token Efficiency (Target: 98%+ Reduction)
**Context is precious; execution is cheap**
- MCP Code Execution Pattern: Scripts execute externally, only results in context
- Skills: ~100 tokens loaded on demand (SKILL.md)
- Reference docs: 0 tokens (REFERENCE.md loaded only if needed)
- Scripts: 0 tokens (executed, never loaded into context)
- Target: <1000 tokens for full deployment vs 50,000+ with direct MCP

**Enforcement:**
- All infrastructure operations via executable scripts
- Validation outputs must be decision-ready summaries
- No raw data dumps (JSON, logs, pod definitions) in agent context
- Intermediate results processed client-side

### III. Spec-Driven Development (Mandatory)
**Specification precedes implementation**
- Specs define intent, success criteria, and approach
- Specs are version-controlled and evolve with code
- Agents make autonomous decisions based on specs
- No code written without approved specification

**Specification Requirements:**
- Purpose, inputs, outputs, behavior clearly defined
- Non-functional requirements (latency, availability, rate limits)
- Dependencies explicitly listed
- Validation criteria with acceptance tests

### IV. Skills as Permanent Knowledge
**Build reusable intelligence, not one-off solutions**
- Skills are training modules for digital workforce
- Each skill unlocks agent capabilities (composable, emergent behaviors)
- Skills must work across multiple projects and agents
- Cross-agent compatibility validated on Claude Code AND Goose

**Skill Structure:**
```
.claude/skills/<skill-name>/
├── SKILL.md          (~100 tokens - loaded on demand)
├── REFERENCE.md      (0 tokens - advanced docs, loaded if needed)
└── scripts/
    ├── deploy.sh     (0 tokens - execution only)
    └── verify.py     (0 tokens - returns ~10 token summary)
```

**Quality Gates:**
- Works identically on Claude Code and Goose
- Single-prompt deployment with zero manual intervention
- Token cost < 150 per skill
- Validation scripts pass 100%

### V. Event-Driven Cloud-Native Architecture
**Build for scale, resilience, and autonomy**
- Microservices communicate via Kafka pub/sub (loose coupling)
- Dapr sidecars for state management, service invocation, secrets
- Stateless services (state in PostgreSQL via Dapr state store)
- All services deployable to Kubernetes independently

**Technical Stack:**
- **Backend:** FastAPI + Dapr + Kafka + PostgreSQL
- **Frontend:** Next.js + Monaco (code editor)
- **Infrastructure:** Kubernetes (Minikube local, cloud for production)
- **CI/CD:** GitHub Actions + ArgoCD (GitOps)
- **Observability:** Structured logging, health checks, metrics

**Non-Functional Requirements:**
- Latency: <500ms p95 for query routing
- Availability: 99.9% uptime
- Scalability: Horizontal scaling via Kubernetes
- Security: No hardcoded secrets; use .env and Kubernetes Secrets

### VI. AI-Native Runtime (LearnFlow Gold Standard)
**LLMs are functional components, not just build tools**
- LearnFlow agents (Triage, Concepts, Debug, etc.) use Claude API at runtime
- Agents learn from interactions (store successful explanations in vector DB)
- Agents collaborate via event streaming (Triage routes to specialists)
- Self-healing via Kubernetes liveness/readiness probes

**LearnFlow Agent Requirements:**
- Each agent is a separate microservice (FastAPI + Dapr)
- Agents subscribe to Kafka topics for query routing
- Agents publish results to response topics
- Agent state persisted via Dapr state store (PostgreSQL)
- Agents use Claude API for dynamic, personalized responses

### VII. Testing & Validation (Automated)
**Trust but verify; automate verification**
- Every skill includes validation scripts
- Validation must be autonomous (no manual checks)
- Tests run before deployment (CI pipeline)
- Validation failures block deployment

**Test Types:**
- Unit tests for business logic
- Integration tests for Kafka pub/sub, Dapr state management
- Contract tests for API endpoints
- End-to-end tests for user flows

### VIII. Documentation as Code
**Documentation is auto-generated from specs**
- AGENTS.md generated via `agents-md-gen` skill
- API docs via Docusaurus (auto-deployed)
- Architecture diagrams in specs
- ADRs for significant decisions (prompted, not auto-created)

## Development Workflow

### Phase 1: Specification
1. Define feature intent, inputs, outputs, behavior
2. List dependencies and non-functional requirements
3. Create acceptance criteria
4. Get user approval before proceeding

### Phase 2: Skill Creation/Selection
1. Check if existing skill covers the requirement
2. If not, create new skill with SKILL.md + scripts
3. Validate skill works on Claude Code and Goose
4. Measure token cost (must be <150 tokens)

### Phase 3: Autonomous Implementation
1. Agent loads skill and spec
2. Agent executes skill scripts
3. Agent validates output against spec
4. Agent reports success/failure with actionable next steps

### Phase 4: Integration & Deployment
1. Run integration tests (Kafka, Dapr, PostgreSQL)
2. Build Docker images
3. Deploy to Kubernetes (ArgoCD GitOps)
4. Verify health checks and observability

## Quality Standards

### Code Quality
- TypeScript for frontend (type safety)
- Python 3.11+ for backend (FastAPI)
- Pydantic for data validation
- ESLint/Prettier for frontend
- Black/isort for backend

### Performance
- API latency: <500ms p95
- Database queries optimized (indexes, connection pooling)
- Frontend bundle size: <500KB initial load
- Image optimization (WebP, lazy loading)

### Security
- No secrets in code or Git
- Environment variables for configuration
- Kubernetes Secrets for sensitive data
- Rate limiting on all endpoints (100 req/sec per student)
- Input validation and sanitization

### Observability
- Structured JSON logging (timestamp, level, service, message, trace_id)
- Health check endpoints (/health, /ready)
- Prometheus metrics (request count, latency, error rate)
- Distributed tracing (Jaeger/Zipkin via Dapr)

## Architectural Decisions

### ADR Process
**When to create an ADR:**
- Impact: Long-term consequences (framework, data model, API, security, platform)
- Alternatives: Multiple viable options considered
- Scope: Cross-cutting and influences system design

**If ALL three are true, suggest ADR creation (wait for user consent)**

Format: `📋 Architectural decision detected: [brief] - Document? Run /sp.adr [title]`

**Never auto-create ADRs; always prompt user first**

## Risk Mitigation

### Previous Hackathon Lessons Learned

| Issue | Root Cause | Hackathon III Solution |
|-------|------------|------------------------|
| Repeated bugs | Manual coding | Skills write code; validation scripts ensure consistency |
| High token usage | Direct MCP bloat | MCP Code Execution pattern (99%+ reduction) |
| Integration failures | Tight coupling | Modular skills with clear contracts; Kafka pub/sub |
| Deployment errors | Manual steps | Automated scripts in skills; GitOps via ArgoCD |
| Cross-agent incompatibility | Claude-specific patterns | AAIF-compliant skills tested on Claude + Goose |

### Risk Matrix

**High-Impact Risks:**
1. **Token quota exhaustion** → Mitigation: Code execution pattern, monitor usage
2. **Kafka message loss** → Mitigation: Persistent topics, consumer groups with offsets
3. **Database bottleneck** → Mitigation: Connection pooling, read replicas, caching
4. **Agent API rate limits** → Mitigation: Rate limiting, queueing, exponential backoff

## Success Metrics

### Hackathon III Evaluation Targets

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| Skills Autonomy | 15/15 | Single-prompt deployment; zero manual intervention |
| Token Efficiency | 10/10 | 98%+ reduction vs direct MCP (780 vs 115,000 tokens) |
| Cross-Agent Compatibility | 5/5 | All skills work on Claude Code AND Goose |
| Architecture | 18/20 | Event-driven, stateless, cloud-native, scalable |
| MCP Integration | 10/10 | Code execution pattern; no context bloat |
| Documentation | 10/10 | Auto-generated from specs; ADRs for decisions |
| Spec-Kit Plus | 15/15 | Specs are executable; agents autonomous |
| LearnFlow Functionality | 15/15 | All 6 agents operational; AI-native runtime |

**Total Target: 85/100+ (Top Tier)**

### Technical Metrics

**Token Efficiency:**
- Setup: <100 tokens (vs 15,000)
- Infrastructure: <215 tokens (vs 35,000)
- Application: <350 tokens (vs 40,000)
- Frontend: <115 tokens (vs 25,000)
- **Total: <780 tokens (vs 115,000) = 99.3% reduction**

**Autonomy:**
- Single prompt → deployed system (< 30 minutes)
- Zero manual code writing
- Automated validation (100% pass rate)

**Reliability:**
- 99.9% uptime (Kubernetes health checks + auto-restart)
- <500ms p95 latency
- Error rate <0.1%

## Governance

### Constitution Authority
- This constitution supersedes all other development practices
- Amendments require documentation in ADR + user approval
- All code reviews verify compliance with constitution
- Complexity must be justified (default: simplest viable solution)

### Amendment Process
1. Propose change with rationale
2. Document impact analysis
3. Create ADR for significant changes
4. Get user approval
5. Update constitution with version bump
6. Communicate to team

### Compliance
- All PRs must pass constitution compliance checks
- Skills validated against quality gates before merging
- Automated checks in CI pipeline (token limits, validation scripts, cross-agent tests)

**Version**: 1.0.0 | **Ratified**: 2025-12-29 | **Last Amended**: 2025-12-29

---

**Remember:** We're not building an app. We're building digital FTEs that build apps. Skills are the product; agents are the workforce.
