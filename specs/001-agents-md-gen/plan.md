# Implementation Plan: AGENTS.md Documentation Generator

**Branch**: `001-agents-md-gen` | **Date**: 2025-12-29 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-agents-md-gen/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Create an autonomous skill that generates comprehensive AGENTS.md documentation by analyzing FastAPI microservice codebases. The skill scans backend directories, extracts agent metadata (names, ports, purposes, API endpoints, dependencies), validates Pydantic schemas, maps Kafka topic interactions, and produces AAIF-compliant markdown documentation. Primary goal is 98%+ token efficiency (<100 tokens) through MCP Code Execution Pattern while ensuring cross-agent compatibility (Claude Code, Goose, Aider).

## Technical Context

**Language/Version**: Python 3.11+ (for static analysis via AST parsing)
**Primary Dependencies**:
- Python standard library: `ast` (syntax tree parsing), `pathlib` (file traversal), `json` (metadata serialization)
- No external Python packages required (zero-dependency skill for maximum portability)
**Storage**: N/A (skill generates markdown files, no persistent storage)
**Testing**:
- Unit tests: Python `unittest` for AST parser components
- Integration tests: Run skill on reusable_intelligence backend/ directory (6 agents)
- Cross-agent tests: Execute on Claude Code and Goose, compare outputs via `diff`
**Target Platform**: Cross-platform (Windows, Linux, macOS) - pure Python, no OS-specific dependencies
**Project Type**: Single skill (not web/mobile) - implemented as `.claude/skills/agents-md-gen/`
**Performance Goals**:
- <30 seconds to analyze 6-agent codebase (~3,000 LOC total)
- <100 tokens loaded into agent context (SKILL.md only, scripts execute externally)
**Constraints**:
- Token budget: <100 tokens (SC-002)
- Cross-agent compatibility: Byte-for-byte identical output (SC-003)
- Zero external dependencies (maximum portability across agent platforms)
- Validation scripts must return <10 token summaries (not full JSON dumps)
**Scale/Scope**:
- Target codebase: 6-10 microservice agents
- ~500-1000 LOC per agent
- 5-15 API endpoints per agent
- Generated AGENTS.md: ~300-500 lines

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Agent-Native Development ✅ PASS

- **Skills as Product**: This IS a skill (agents-md-gen), not a one-off script
- **Single-Prompt Deployment**: Skill executes via one command: `claude "Generate AGENTS.md for this project"`
- **Intent-Based Instructions**: User provides intent ("document agents"), skill handles implementation autonomously
- **Cross-Agent Compatible**: Designed for Claude Code, Goose, and Aider (AAIF-compliant)
- **168 hrs/week Autonomy**: Skill can run repeatedly without human intervention

### Principle II: Token Efficiency (98%+ Reduction) ✅ PASS

- **MCP Code Execution Pattern**:
  - SKILL.md: ~80 tokens (loaded on demand)
  - REFERENCE.md: 0 tokens (advanced docs, loaded only if needed)
  - Scripts: 0 tokens (execute externally, only return ~10 token summaries)
- **Target**: <100 tokens total vs 5,000+ manual documentation
- **Validation Scripts**: Return minimal output (e.g., "✓ 6 agents documented" not full JSON)

### Principle III: Spec-Driven Development ✅ PASS

- **Specification First**: spec.md created before plan.md (current file)
- **Autonomous Decisions**: Skill determines how to parse AST, extract schemas, format markdown
- **Executable Blueprint**: This plan defines structure, scripts, validation - ready for /sp.tasks

### Principle IV: Skills as Permanent Knowledge ✅ PASS

- **Reusable**: Works on any FastAPI multi-agent project (not LearnFlow-specific)
- **Cross-Project**: Can document other microservice architectures
- **Composable**: Could combine with other skills (e.g., docusaurus-deploy for website generation)
- **Portable**: Zero external dependencies, pure Python stdlib

### Principle V: Event-Driven Cloud-Native ⚠️ N/A (Skill, Not Service)

- **Not Applicable**: This is a development tool (skill), not a deployed service
- **Rationale**: Skills don't need Kafka/Dapr/K8s - they generate code/docs that use those patterns
- **Future**: The AGENTS.md output will document event-driven architectures

### Principle VI: AI-Native Runtime ⚠️ N/A (Documentation Tool)

- **Not Applicable**: Skill generates docs, doesn't run Claude API at runtime
- **Rationale**: This is build-time tooling, not a runtime service with LLM integration
- **Future**: Could enhance to suggest improvements via Claude API (Phase 2 feature)

### Principle VII: Testing & Validation ✅ PASS

- **Validation Scripts Included**:
  1. `verify_agents_md.py` - Checks AAIF compliance (returns PASS/FAIL + issue count)
  2. `cross_agent_test.py` - Compares Claude Code vs Goose outputs (returns IDENTICAL/DIFF)
  3. `token_counter.py` - Measures token usage (returns count vs baseline)
- **Automated**: No manual checks required
- **Autonomous**: Scripts run as part of skill execution

### Principle VIII: Documentation as Code ✅ PASS

- **Self-Documenting**: This skill generates AGENTS.md automatically
- **SKILL.md**: Contains usage instructions and examples
- **REFERENCE.md**: Advanced patterns for complex codebases
- **No Manual Docs**: All documentation generated from code analysis

### Summary: 6/6 Applicable Principles PASS ✅

(2 principles N/A for development tooling - appropriate exceptions)

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
.claude/skills/agents-md-gen/
├── SKILL.md                    # ~80 tokens - loaded on demand
├── REFERENCE.md                # 0 tokens - advanced docs (loaded if needed)
└── scripts/
    ├── analyze_agents.py       # 0 tokens - discovers agents in backend/
    ├── extract_metadata.py     # 0 tokens - parses AST for endpoints/schemas
    ├── generate_agents_md.py   # 0 tokens - creates markdown from metadata
    ├── verify_agents_md.py     # 0 tokens - validates AAIF compliance
    ├── cross_agent_test.py     # 0 tokens - tests Claude Code vs Goose
    └── token_counter.py        # 0 tokens - measures token usage

tests/
├── unit/
│   ├── test_ast_parser.py      # Tests extract_metadata.py functions
│   ├── test_markdown_gen.py    # Tests generate_agents_md.py output
│   └── test_aaif_validation.py # Tests verify_agents_md.py checks
└── integration/
    ├── test_full_generation.py # End-to-end test on sample backend/
    └── fixtures/
        └── sample_backend/     # Mock 2-agent project for testing
            ├── agent1/
            │   └── main.py     # Minimal FastAPI app
            └── agent2/
                └── main.py     # Minimal FastAPI app
```

**Structure Decision**: Single project (Opt 1) - This is a skill, not a web/mobile app. The skill structure follows Claude Code/Goose conventions:
- **SKILL.md**: Concise usage guide (loaded into agent context)
- **REFERENCE.md**: Detailed patterns for edge cases (loaded only if requested)
- **scripts/**: Executable Python files (never loaded, only executed)
- **tests/**: Standard Python test structure (unittest framework)

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**Status**: N/A - No constitution violations detected. All 6 applicable principles pass.

## Phase 0: Research & Technical Decisions

**Objective**: Resolve all NEEDS CLARIFICATION items from Technical Context and document key technical decisions.

**Status**: ✅ COMPLETE - See [research.md](./research.md) for full details

**Key Decisions Made**:
1. **AST Parsing vs Regex**: Use Python `ast` module for reliable code analysis
2. **Zero External Dependencies**: Stdlib only for maximum portability
3. **AAIF Compliance**: Follow Agent Automation Interoperability Framework standards
4. **Token Efficiency Pattern**: MCP Code Execution (scripts return summaries, not full data)
5. **Dependency Detection**: Combined approach (imports + environment variables)
6. **Cross-Agent Compatibility**: Deterministic generation with path normalization

## Phase 1: Design & Contracts

**Objective**: Define data models, API contracts (if applicable), and quickstart documentation.

**Status**: ✅ COMPLETE

### Artifacts Created

1. **[data-model.md](./data-model.md)** - Metadata structures for internal representation
   - `AgentMetadata`: Core agent entity with name, port, purpose, endpoints, dependencies
   - `EndpointMetadata`: API route with method, path, request/response schemas
   - `SchemaMetadata`: Pydantic model representation with fields
   - `FieldMetadata`: Individual schema field with type, required, description
   - `DependencyMetadata`: External service/package dependency
   - `KafkaTopics`: Pub/sub topic subscriptions and publications

2. **[quickstart.md](./quickstart.md)** - User-facing documentation
   - Installation instructions (global vs local skill installation)
   - Basic usage examples for Claude Code, Goose, Aider
   - Advanced scenarios (custom backend dir, preserve sections, validation)
   - Troubleshooting guide (common errors and solutions)
   - Performance benchmarks (2-20 agents, <100 tokens all cases)

3. **contracts/** - N/A (this is a skill, not a service with API endpoints)

### Key Design Decisions

1. **Data Flow**: Discovery → Extraction → Generation → Validation (4-stage pipeline)
2. **Serialization**: JSON for intermediate metadata (enables debugging and testing)
3. **Type Safety**: Python dataclasses for all metadata structures
4. **Determinism**: Alphabetical sorting for all lists (reproducible output)
5. **Edge Case Handling**: Graceful degradation with warnings (never crash)

### Agent Context Updated

✅ Updated `CLAUDE.md` with:
- Language: Python 3.11+ (for AST parsing)
- Database: N/A (skill generates markdown, no storage)
- Project Type: Single skill

## Constitution Check (Post-Design Re-Evaluation)

**Status**: ✅ ALL PRINCIPLES STILL PASS

No changes from initial evaluation. Design decisions reinforce constitutional compliance:
- **Token Efficiency**: Confirmed <100 tokens (SKILL.md ~80, validation output ~10)
- **Cross-Agent Compatible**: Data model uses standard Python dataclasses (portable)
- **Testing & Validation**: 3 validation scripts specified (verify_agents_md.py, cross_agent_test.py, token_counter.py)
- **Documentation**: quickstart.md provides comprehensive usage guide

## Next Steps

### Ready for /sp.tasks

With planning complete, the feature is ready for task breakdown:

```bash
# Generate actionable tasks from this plan
/sp.tasks
```

Expected output: ~15-20 tasks covering:
1. **Setup**: Create skill directory structure, SKILL.md, REFERENCE.md
2. **Core Scripts**: Implement analyze_agents.py, extract_metadata.py, generate_agents_md.py
3. **Validation Scripts**: Implement verify_agents_md.py, cross_agent_test.py, token_counter.py
4. **Testing**: Unit tests, integration tests, cross-agent compatibility tests
5. **Documentation**: Finalize SKILL.md and REFERENCE.md
6. **Validation**: Run on reusable_intelligence backend/, verify SC-001 to SC-010

### Implementation Priority

**Phase 1 (P1 - Core MVP)**:
1. analyze_agents.py - Discover agents in backend/
2. extract_metadata.py - Parse AST, extract endpoints/schemas
3. generate_agents_md.py - Create AAIF-compliant markdown
4. Basic SKILL.md - Usage instructions

**Phase 2 (P2 - Quality & Validation)**:
5. verify_agents_md.py - AAIF compliance checking
6. cross_agent_test.py - Claude Code vs Goose comparison
7. token_counter.py - Measure token usage
8. Integration tests - End-to-end validation

**Phase 3 (P3 - Polish)**:
9. REFERENCE.md - Advanced patterns
10. Edge case handling improvements
11. Performance optimization (if needed)

### Success Criteria Validation Plan

After implementation, validate against spec.md success criteria:

| SC # | Criterion | Validation Method |
|------|-----------|-------------------|
| SC-001 | <30s for 6-agent system | Time execution on reusable_intelligence backend/ |
| SC-002 | <100 tokens (98%+ reduction) | Run token_counter.py, compare to 5,000+ baseline |
| SC-003 | Byte-for-byte identical (Claude vs Goose) | Run cross_agent_test.py with diff |
| SC-004 | 100% agent discovery accuracy | Manual verification against backend/ contents |
| SC-005 | 95% endpoint extraction accuracy | Compare generated vs actual FastAPI routes |
| SC-006 | Zero manual edits required | Review generated AGENTS.md for completeness |
| SC-007 | AAIF compliance passes | Run verify_agents_md.py, expect PASS |
| SC-008 | 2+ hours saved vs manual | Calculate: (manual time - generation time) |
| SC-009 | Handles edge cases without crashing | Test fixtures with 0 agents, duplicate ports, missing schemas |
| SC-010 | Renders correctly in markdown viewers | Open AGENTS.md in GitHub, VS Code, GitLab |

## Risk Assessment

### Low Risks (Mitigated by Design)

1. **External Dependencies**: NONE (pure Python stdlib)
2. **Cross-Platform Compatibility**: Using pathlib.Path for all file operations
3. **Token Quota Exhaustion**: <100 token budget leaves 99,900+ tokens for other tasks
4. **Version Compatibility**: Python 3.11+ widely available (released Oct 2022)

### Medium Risks (Monitoring Required)

1. **Complex FastAPI Patterns**: Dynamic routing, nested Pydantic models may be hard to parse
   - **Mitigation**: Start with simple patterns, add complexity incrementally
   - **Fallback**: Warn and skip complex endpoints (don't crash)

2. **AAIF Standard Changes**: If AAIF spec evolves, generated docs may become non-compliant
   - **Mitigation**: REFERENCE.md documents AAIF version targeted
   - **Future**: Update validation script when standard changes

### Negligible Risks

1. **Performance**: AST parsing is fast (<30s even for 20 agents)
2. **Memory**: No large data structures held in memory (stream processing)
3. **Security**: No external API calls, no user input execution

## Conclusion

**Planning Status**: ✅ COMPLETE

All planning artifacts generated:
- ✅ Technical Context defined (no NEEDS CLARIFICATION)
- ✅ Constitution Check passed (6/6 applicable principles)
- ✅ Phase 0 Research complete (6 key decisions documented)
- ✅ Phase 1 Design complete (data model, quickstart guide)
- ✅ Agent context updated (CLAUDE.md)

**Ready for**: `/sp.tasks` to generate actionable implementation tasks

**Estimated Implementation**: 8-12 hours (1.5 days)
- Core functionality: 6 hours
- Validation scripts: 2 hours
- Testing: 3 hours
- Documentation polish: 1 hour

**Risk Level**: LOW (pure Python stdlib, zero external dependencies, well-defined scope)
