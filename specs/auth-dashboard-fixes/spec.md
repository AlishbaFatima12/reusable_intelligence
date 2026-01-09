# Auth & Dashboard Critical Bug Fixes

**Feature:** auth-dashboard-fixes
**Priority:** P0 (Production Blocking)
**Status:** In Progress

---

## User Stories

### [P0] US1: Role-Based Authentication Enforcement

**As a** system administrator
**I want** users to login with their registered role only
**So that** teachers cannot access student dashboards and vice versa

**Acceptance Criteria:**
- [ ] Teacher email (alishbafatima73@gmail.com) CANNOT login as Student
- [ ] Student email (alishbafatima25@gmail.com) CANNOT login as Teacher
- [ ] Auth API validates role matches registered role
- [ ] Clear error message: "This account is registered as [ROLE]. Please select [ROLE] to login."
- [ ] Toggle position matches registered role on error

**Current Bug:**
- Teacher email can login as student → shows teacher dashboard (wrong!)
- No validation between registered role and selected role at login

---

### [P0] US2: Mastery Percentage Display Fix

**As a** student
**I want** accurate mastery percentages after practice
**So that** I can track my learning progress correctly

**Acceptance Criteria:**
- [ ] Backend: 5 topics = 100% total (each worth 20%) ✅ DONE
- [ ] Frontend: Displays backend percentages correctly
- [ ] Topic mastery: 0-100% per topic
- [ ] Overall mastery: sum(all topics) / 500
- [ ] Practice once (3/3) → Topic: 10%, Overall: 2%
- [ ] Practice 10 times → Topic: 100%, Overall: 20%

**Current Bug:**
- Backend formula fixed but frontend may cache old data
- Need to verify display logic matches backend calculations

---

### [P1] US3: Teacher Dashboard Functions

**As a** teacher
**I want** all dashboard buttons to work
**So that** I can generate and assign tests to students

**Acceptance Criteria:**
- [ ] GENERATE TEST button creates MCQs instantly
- [ ] ASSIGN TO SELECTED loads students and assigns test
- [ ] AUTO-ASSIGN detects struggling students (<40%) and assigns
- [ ] Student sees assigned tests in practice panel
- [ ] Student receives notification badge for new assignments

**Current Bug:**
- User reports buttons not working (need to verify)
- Generated tests not appearing in student dashboard

---

### [P1] US4: Concepts Agent Real Responses

**As a** student
**I want** real explanations for Python concepts
**So that** I can learn effectively

**Acceptance Criteria:**
- [ ] Concepts Agent calls Claude API successfully
- [ ] Returns actual explanations (not fallback message)
- [ ] Handles API key errors gracefully
- [ ] Timeout set appropriately (30s)

**Current Bug:**
- Returns: "Due to a temporary issue..." fallback message
- Likely missing/invalid ANTHROPIC_API_KEY in .env

---

## Technical Context

**Files:**
- Frontend: `mystery-skils-app-ui/public/mystery-skills-flash.html`
- Backend Auth: `mystery-skils-app-ui/app/api/auth/login/route.ts`
- Progress Tracker: `backend/agents/progress/services/tracker.py`
- Concepts Agent: `backend/agents/concepts/services/explainer.py`

**Tech Stack:**
- Frontend: Vanilla JavaScript (embedded in HTML)
- Backend: Next.js 15 (auth), FastAPI (agents)
- Database: NeonDB PostgreSQL (via Prisma)
- Auth: Custom endpoints (simplified from better-auth)

---

## Out of Scope

- New features or redesigns
- Performance optimization beyond bug fixes
- Additional test coverage
- Documentation updates
