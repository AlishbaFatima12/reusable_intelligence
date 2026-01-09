# Tasks: Auth & Dashboard Critical Bug Fixes

**Feature:** auth-dashboard-fixes
**Generated:** 2026-01-08
**Total Tasks:** 15

---

## Phase 1: Setup & Analysis

### Story Goal
Understand current system state and prepare for fixes

### Tasks
- [X] T001 Verify backend Progress Tracker running with new mastery formula (port 8006)
- [ ] T002 Test current auth flow: teacher login as student (should fail, currently doesn't)
- [ ] T003 Test current auth flow: student login as teacher (should fail, currently doesn't)
- [X] T004 Check .env for ANTHROPIC_API_KEY presence and validity

---

## Phase 2: [P0] US1 - Role-Based Authentication Enforcement

### Story Goal
Prevent cross-role login (teacher as student, student as teacher)

### Independent Test Criteria
- ✅ Teacher email + Student role → Rejected with error
- ✅ Student email + Teacher role → Rejected with error
- ✅ Teacher email + Teacher role → Success
- ✅ Student email + Student role → Success

### Tasks
- [X] T005 [US1] Read auth login route in mystery-skils-app-ui/app/api/auth/login/route.ts
- [X] T006 [US1] Add role validation: fetch user from DB, compare stored role with selected role
- [X] T007 [US1] Return error if roles mismatch: `{success: false, error: "This account is registered as TEACHER. Please select TEACHER to login."}`
- [X] T008 [US1] Update frontend login handler in mystery-skills-flash.html to show role mismatch error
- [ ] T009 [US1] Test: alishbafatima73@gmail.com (teacher) + Student toggle → Rejected ✅
- [ ] T010 [US1] Test: alishbafatima25@gmail.com (student) + Teacher toggle → Rejected ✅

---

## Phase 3: [P0] US2 - Mastery Percentage Display Fix

### Story Goal
Display accurate mastery percentages matching backend calculations

### Independent Test Criteria
- ✅ Practice once (3/3 correct) → Topic: 10%, Overall: 2%
- ✅ Practice 10 times → Topic: 100%, Overall: 20%
- ✅ All 5 topics at 100% → Overall: 100%

### Tasks
- [ ] T011 [US2] Hard refresh browser (CTRL+SHIFT+R) to clear cached JavaScript
- [ ] T012 [US2] Test backend API: `curl http://localhost:8006/api/v1/mastery/student-1767812047667`
- [ ] T013 [US2] Verify overall_mastery calculation: overall = sum(topics) / 500
- [ ] T014 [US2] Compare backend response with frontend display in browser console
- [ ] T015 [P] [US2] If mismatch: Debug displayStudentMastery() function in mystery-skills-flash.html lines 568-640
- [ ] T016 [US2] Test: Do 1 practice → Check overall shows 2% (not 10%)
- [ ] T017 [US2] Test: Do 10 practices → Check overall shows 20%

---

## Phase 4: [P1] US3 - Teacher Dashboard Functions

### Story Goal
All teacher buttons work and students see assigned tests

### Independent Test Criteria
- ✅ GENERATE TEST creates MCQs visible in console
- ✅ ASSIGN TO SELECTED shows student checkboxes
- ✅ AUTO-ASSIGN detects struggling students
- ✅ Student sees assigned tests in practice panel
- ✅ Student sees notification badge

### Tasks
- [ ] T018 [US3] Test GENERATE TEST button: Click and verify MCQs appear in console-content
- [ ] T019 [US3] If broken: Check browser console (F12) for JavaScript errors
- [ ] T020 [P] [US3] Verify teacherGeneratePractice() function exists in mystery-skills-flash.html line 1737
- [ ] T021 [P] [US3] Verify onclick="teacherGeneratePractice()" binding in HTML line 381
- [ ] T022 [US3] Test ASSIGN TO SELECTED: Verify student checkboxes load
- [ ] T023 [US3] Test AUTO-ASSIGN: Verify struggling students detected
- [ ] T024 [US3] Add assigned tests display section to student practice panel in mystery-skills-flash.html
- [ ] T025 [US3] Read assignedTests from localStorage and filter by studentId
- [ ] T026 [US3] Display assigned tests with "Start Test" button
- [ ] T027 [US3] Add notification badge showing count of unfinished assignments
- [ ] T028 [US3] Test complete flow: Teacher assigns → Student sees notification → Student completes test

---

## Phase 5: [P1] US4 - Concepts Agent Real Responses

### Story Goal
Concepts Agent returns actual Claude API responses instead of fallback

### Independent Test Criteria
- ✅ Ask "explain loops" → Get detailed explanation (not fallback)
- ✅ Ask "what are functions" → Get code examples
- ✅ API errors handled gracefully with retry suggestion

### Tasks
- [ ] T029 [US4] Check Concepts Agent logs (terminal port 8002) for API errors
- [ ] T030 [US4] Verify ANTHROPIC_API_KEY in D:\reuse-skills\.env
- [ ] T031 [US4] If missing: Add key to .env file
- [ ] T032 [US4] Test API key: `curl https://api.anthropic.com/v1/messages -H "x-api-key: KEY"`
- [ ] T033 [P] [US4] Increase timeout in backend/agents/concepts/config.py (30s → 60s)
- [ ] T034 [P] [US4] Add hardcoded fallback explanations for demo in explainer.py line 146
- [ ] T035 [US4] Restart Concepts Agent: `uvicorn backend.agents.concepts.main:app --port 8002 --reload`
- [ ] T036 [US4] Test: Ask "explain Python loops" → Verify real explanation returned

---

## Phase 6: Polish & Verification

### Tasks
- [ ] T037 [P] Clear browser cache and localStorage: `localStorage.clear()`
- [ ] T038 [P] Test complete student workflow: Register → Login → Practice → Check mastery
- [ ] T039 [P] Test complete teacher workflow: Login → Generate test → Assign → Verify student sees it
- [ ] T040 Test cross-role prevention: Teacher tries student login → Rejected ✅
- [ ] T041 Update WORK_SUMMARY_SESSION.md with all fixes applied

---

## Dependencies

```
Phase 1 (Setup)
    ↓
Phase 2 (US1 Auth) ──┐
Phase 3 (US2 Mastery)──┼─→ Phase 6 (Polish)
Phase 4 (US3 Teacher) ──┤
Phase 5 (US4 Concepts)──┘
```

**Phases 2-5 are INDEPENDENT** - can be done in parallel!

---

## Parallel Execution Examples

### US1 (Auth) - Sequential
```
T005 → T006 → T007 → T008 → T009 → T010
```

### US2 (Mastery) - Partially Parallel
```
T011 → T012 → T013 → T014 → (T015 || T016) → T017
```

### US3 (Teacher) - Parallel Groups
```
Group A: T018 → T019 → T020 → T021
Group B (parallel): T022, T023
Group C: T024 → T025 → T026 → T027 → T028
```

### US4 (Concepts) - Parallel Options
```
T029 → T030 → T031 → T032 → (T033 || T034) → T035 → T036
```

---

## Implementation Strategy

**MVP Scope: US1 + US2** (Auth fixes + Mastery display)
- These are P0 production blockers
- Should be fixed FIRST before anything else

**Phase 2 Delivery: US3** (Teacher functions)
- P1 priority, needed for teacher demo

**Phase 3 Delivery: US4** (Concepts Agent)
- Can use fallback for demo if API key unavailable

---

## Validation Checklist

Before marking feature complete:

- [ ] Teacher cannot login as Student ✅
- [ ] Student cannot login as Teacher ✅
- [ ] Mastery percentages accurate (2% per practice, 20% per topic mastered)
- [ ] Teacher GENERATE TEST works
- [ ] Teacher ASSIGN works
- [ ] Student sees assigned tests
- [ ] Concepts Agent returns real explanations (or acceptable fallback)
- [ ] All tests passing
- [ ] Documentation updated (WORK_SUMMARY_SESSION.md)

---

**Total Estimated Tasks:** 41
**Parallelizable Tasks:** 12 marked with [P]
**Critical Path:** US1 (6 tasks) → US2 (7 tasks) → Verification (5 tasks)
**Minimum Time:** 18 sequential tasks if parallelized optimally
