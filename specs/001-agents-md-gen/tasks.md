# Implementation Tasks: AGENTS.md Documentation Generator

**Feature**: 001-agents-md-gen
**Branch**: `001-agents-md-gen`
**Spec**: [spec.md](./spec.md)
**Plan**: [plan.md](./plan.md)

## Overview

This document breaks down the implementation into actionable tasks organized by user story priority. Each user story represents an independently testable increment that delivers value.

**Total Tasks**: 24
**Estimated Time**: 8-12 hours

## User Story Mapping

| User Story | Priority | Tasks | Description |
|------------|----------|-------|-------------|
| US1 - Auto-Generate Documentation | P1 (MVP) | T003-T012 | Core capability: scan agents, extract metadata, generate AGENTS.md |
| US2 - Cross-Agent Compatibility | P2 | T013-T017 | Validation: AAIF compliance, cross-agent testing |
| US3 - Token Efficiency Reporting | P3 | T018-T020 | Metrics: token counting and reporting |

## Implementation Strategy

**MVP Scope (Ship First)**:
- Complete Phase 1 (Setup) + Phase 2 (Foundational) + Phase 3 (User Story 1)
- Delivers core value: automated AGENTS.md generation
- Estimated: 6 hours

**Incremental Delivery**:
- Phase 4 (US2): Add validation and cross-agent compatibility
- Phase 5 (US3): Add token efficiency metrics
- Phase 6: Polish and edge cases

## Dependency Graph

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational - Data Model)
    ↓
Phase 3 (US1 - Core Generation) ← MVP DELIVERABLE
    ↓
Phase 4 (US2 - Validation) ← Can run in parallel with Phase 5
    ↓
Phase 5 (US3 - Metrics) ← Can run in parallel with Phase 4
    ↓
Phase 6 (Polish)
```

**Parallel Execution Opportunities**:
- Phase 4 and Phase 5 are independent (can run in parallel)
- Within phases: Tasks marked [P] can run in parallel

---

## Phase 1: Setup & Infrastructure

**Goal**: Initialize skill directory structure and base documentation

**Tasks**:

- [x] T001 Create skill directory structure at .claude/skills/agents-md-gen/ with subdirectories: scripts/, tests/unit/, tests/integration/fixtures/sample_backend/
- [x] T002 [P] Create test fixture: sample 2-agent FastAPI project in tests/integration/fixtures/sample_backend/ (agent1/main.py, agent2/main.py)

---

## Phase 2: Foundational - Data Model Implementation

**Goal**: Implement core data structures that all user stories depend on

**Independent Test**: Data model serializes/deserializes correctly to/from JSON

**Tasks**:

- [x] T003 Implement data model classes in .claude/skills/agents-md-gen/scripts/data_model.py (AgentMetadata, EndpointMetadata, SchemaMetadata, FieldMetadata, DependencyMetadata, KafkaTopics as Python dataclasses)

---

## Phase 3: User Story 1 - Auto-Generate Agent Documentation (P1 - MVP)

**Story Goal**: A developer can run the skill on a multi-agent codebase and get a complete AGENTS.md file automatically

**Independent Test**: Run skill on tests/integration/fixtures/sample_backend/, verify AGENTS.md contains both agents with accurate metadata

**Acceptance Criteria**:
- ✅ Discovers all agents in backend/ directory
- ✅ Extracts agent names, ports, purposes from code
- ✅ Parses FastAPI endpoints with request/response schemas
- ✅ Generates AAIF-compliant markdown
- ✅ Handles zero-agent projects gracefully

**Tasks**:

### US1 - Agent Discovery

- [x] T004 [P] [US1] Implement analyze_agents.py: scan_backend_directory(backend_path: Path) → list[Path] that recursively discovers agent directories containing main.py files
- [x] T005 [P] [US1] Implement analyze_agents.py: is_fastapi_agent(agent_dir: Path) → bool that detects FastAPI() instances via AST parsing

### US1 - Metadata Extraction

- [x] T006 [US1] Implement extract_metadata.py: extract_agent_name(agent_dir: Path) → str that derives name from directory
- [x] T007 [US1] Implement extract_metadata.py: extract_port(agent_dir: Path) → int that finds port from .env, config files, or defaults to 8000
- [x] T008 [US1] Implement extract_metadata.py: extract_purpose(agent_dir: Path) → str that gets purpose from module docstring or defaults to "[No description provided]"
- [x] T009 [US1] Implement extract_metadata.py: extract_endpoints(agent_dir: Path) → list[EndpointMetadata] that parses @app.post/@app.get decorators via AST
- [x] T010 [US1] Implement extract_metadata.py: extract_pydantic_schemas(agent_dir: Path) → dict[str, SchemaMetadata] that analyzes Pydantic model classes
- [x] T011 [US1] Implement extract_metadata.py: extract_dependencies(agent_dir: Path) → list[DependencyMetadata] that analyzes imports and .env variables

### US1 - Markdown Generation

- [x] T012 [US1] Implement generate_agents_md.py: generate_markdown(agents: list[AgentMetadata]) → str that creates AAIF-compliant AGENTS.md with sorted agents/endpoints for deterministic output

---

## Phase 4: User Story 2 - Cross-Agent Compatibility Validation (P2)

**Story Goal**: Developers can verify generated docs work identically across Claude Code, Goose, and Aider

**Independent Test**: Generate AGENTS.md twice (simulate different agents), compare byte-for-byte with diff

**Acceptance Criteria**:
- ✅ AAIF validation checks pass
- ✅ Byte-for-byte identical output (deterministic generation)
- ✅ All required sections present
- ✅ Markdown renders correctly

**Tasks**:

### US2 - AAIF Validation

- [x] T013 [P] [US2] Implement verify_agents_md.py: validate_aaif_compliance(md_path: Path) → ValidationReport that checks for required sections (Agent Name, Port, Purpose, Dependencies, API Contract, Pub/Sub)
- [x] T014 [P] [US2] Implement verify_agents_md.py: check_port_conflicts(agents: list[AgentMetadata]) → list[str] that detects duplicate port numbers
- [x] T015 [P] [US2] Implement verify_agents_md.py: format_validation_output(report: ValidationReport) → str that returns concise summary (<10 tokens: "✓ PASS" or "✗ FAIL: 2 warnings")

### US2 - Cross-Agent Testing

- [x] T016 [US2] Implement cross_agent_test.py: compare_outputs(md_path1: Path, md_path2: Path) → bool that performs byte-for-byte comparison and returns True if identical
- [x] T017 [US2] Implement cross_agent_test.py: format_test_output(is_identical: bool) → str that returns concise result (<10 tokens: "✓ IDENTICAL" or "✗ DIFF at line X")

---

## Phase 5: User Story 3 - Token Efficiency Reporting (P3)

**Story Goal**: Developers can measure token usage and validate 98%+ reduction claim

**Independent Test**: Run token counter on SKILL.md and validation outputs, verify total <100 tokens

**Acceptance Criteria**:
- ✅ Accurately counts tokens in SKILL.md
- ✅ Measures validation script outputs
- ✅ Compares to manual baseline (5,000+ tokens)
- ✅ Reports 98%+ reduction

**Tasks**:

### US3 - Token Measurement

- [x] T018 [P] [US3] Implement token_counter.py: count_tokens(text: str) → int using word_count * 1.3 approximation method
- [x] T019 [P] [US3] Implement token_counter.py: measure_skill_tokens() → dict that counts SKILL.md, validation outputs, and calculates total
- [x] T020 [US3] Implement token_counter.py: format_metrics_output(metrics: dict) → str that returns concise report (<10 tokens: "Total: 92 tokens, 98.4% reduction")

---

## Phase 6: Skill Documentation & Polish

**Goal**: Create user-facing documentation and handle edge cases

**Tasks**:

### Skill Documentation

- [x] T021 [P] Create SKILL.md in .claude/skills/agents-md-gen/ with usage instructions (~80 tokens): skill purpose, basic usage example, options (backend_dir parameter)
- [x] T022 [P] Create REFERENCE.md in .claude/skills/agents-md-gen/ with advanced patterns: handling complex FastAPI routes, custom Pydantic validators, preserving custom sections with <!-- PRESERVE --> tags

### Edge Case Handling

- [x] T023 Enhance extract_metadata.py to handle edge cases: empty directories, missing FastAPI apps, duplicate ports (warn), complex routing patterns (warn), missing docstrings (use placeholders)
- [x] T024 Add integration test in tests/integration/test_full_generation.py: end-to-end test that runs all scripts on sample_backend/ and validates AGENTS.md output

---

## Validation Checklist

After completing each user story, validate against success criteria:

### User Story 1 (P1) Validation

- [ ] SC-001: Generation completes in <30 seconds for 6-agent system
- [ ] SC-004: 100% agent discovery accuracy
- [ ] SC-005: 95%+ endpoint extraction accuracy
- [ ] SC-006: Zero manual edits required
- [ ] SC-009: Handles edge cases without crashing (0 agents, duplicate ports, missing schemas)
- [ ] SC-010: AGENTS.md renders correctly in GitHub/VS Code

**Test Command**: Run on reusable_intelligence backend/ directory, verify all 6 agents documented

### User Story 2 (P2) Validation

- [ ] SC-003: Byte-for-byte identical output across agents
- [ ] SC-007: AAIF validation passes on first run

**Test Command**: Generate twice, run `diff agents1.md agents2.md`, expect no differences

### User Story 3 (P3) Validation

- [ ] SC-002: <100 tokens total (SKILL.md ~80, validation outputs ~10)
- [ ] SC-008: Demonstrates 98%+ token reduction vs 5,000+ baseline

**Test Command**: Run token_counter.py, verify total <100 tokens

---

## Parallel Execution Examples

### Within User Story 1 (After T003 complete):
```bash
# Can run in parallel:
Task T004 (analyze_agents.py - scan function) &
Task T005 (analyze_agents.py - fastapi detection) &
Task T006 (extract_metadata.py - name extraction)
```

### After User Story 1 Complete:
```bash
# Can run in parallel:
Phase 4 (US2 - Validation) &
Phase 5 (US3 - Metrics)
```

### Within Phase 6 (Polish):
```bash
# Can run in parallel:
Task T021 (SKILL.md) &
Task T022 (REFERENCE.md)
```

---

## Definition of Done

A user story is considered complete when:

1. **All tasks for that story are checked off**
2. **Independent test passes** (defined in each phase)
3. **Acceptance criteria validated** (checkboxes above)
4. **Integration test passes** (if applicable)
5. **No blockers for next story** (dependencies resolved)

---

## MVP Delivery

**Minimum Viable Product** = Phase 1 + Phase 2 + Phase 3 (User Story 1)

This delivers:
- ✅ Automated AGENTS.md generation
- ✅ AST-based code analysis
- ✅ Pydantic schema extraction
- ✅ AAIF-compliant output
- ✅ Edge case handling

Estimated: **6 hours**

Users can immediately use the skill to document their multi-agent projects, saving 2+ hours per project.

---

## Notes

- **No test tasks**: Tests are not explicitly requested in spec.md. Validation is through integration tests (T024) and manual verification against success criteria.
- **Token budget**: All validation scripts MUST return <10 token summaries (not JSON dumps) to meet SC-002.
- **Deterministic output**: All lists (agents, endpoints, fields) MUST be sorted alphabetically for cross-agent compatibility (SC-003).
- **Cross-platform**: Use pathlib.Path throughout for Windows/Linux/macOS compatibility.
