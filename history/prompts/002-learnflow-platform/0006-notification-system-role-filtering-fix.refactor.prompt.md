---
id: 0006
title: Notification System Role-Based Filtering Fix
stage: refactor
date: 2026-01-09
surface: agent
model: claude-opus-4-5-20251101
feature: 002-learnflow-platform
branch: 002-learnflow-platform
user: Ahsan
command: debug-notifications
labels: ["notifications", "role-filtering", "debugging", "instant-popups", "skill-creation"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - mystery-skils-app-ui/public/mystery-skills-flash.html
  - mystery-skils-app-ui/app/api/notifications/[userId]/route.ts
  - mystery-skils-app-ui/app/api/notifications/route.ts
  - mystery-skils-app-ui/app/api/notifications/[userId]/mark-read/route.ts
  - .claude/skills/learnflow-dashboard-debugger/skill.json
  - .claude/skills/learnflow-dashboard-debugger/prompt.md
  - .claude/skills/learnflow-dashboard-debugger/QUICK_FIX.md
tests:
  - Manual test: Teacher sends note to student Alishba
  - Manual test: Student receives instant popup notification
  - Manual test: Notification panel shows correct user ID
---

## Prompt

User reported multiple issues with the notification system:
1. Students seeing teacher notifications in their notification panel
2. Notification popups not appearing instantly when teacher sends notes
3. All old notifications appearing as popups on login
4. Need for a debugging skill to handle dashboard issues efficiently

User messages:
- "the notification button student dashboard shows teachers notification, thats wrong every user student must see their notification"
- "when teacher send notes to student student at the same time receive the note not after signing in again, pops and notification must be instant like facebook"
- "student receive all popups when signing in, all popups all together this approach is no good"

## Response snapshot

### Changes Implemented:

1. **Notification API Role-Based Filtering** (`app/api/notifications/[userId]/route.ts`):
   - Teachers: Only see `completion`, `confirmation`, `registration` types
   - Students: Only see `assignment`, `reminder`, `appreciation`, `encouragement`, `achievement` types
   - Role detection based on userId prefix (`teacher-` vs `student-`)

2. **Debug Logging Added**:
   - Frontend: `[Notifications]` prefix logs showing user role, teacherId, studentId, and notifyId
   - API: `[Notifications API]` logs showing request details, filtering types, and notification counts

3. **Visual User ID Indicator**:
   - Notification panel header now shows: "STUDENT: student-xxxxx" or "TEACHER: teacher-xxxxx"
   - Color-coded: Green for teacher, Blue for student

4. **Instant Popup System**:
   - `seenNotificationIds` Set tracks processed notifications
   - First load: Marks all existing as "seen" (no popups)
   - Subsequent loads: Only shows popups for TRULY NEW notifications
   - 1-second polling interval for near real-time delivery

5. **LearnFlow Dashboard Debugger Skill Created**:
   - Comprehensive debugging guide with issue patterns and fixes
   - Quick reference for common bugs (QUICK_FIX.md)
   - Covers: auth, role-based UI, notifications, page navigation, exercise generation

### Verification:
```
[Notifications API] userId=student-1767970006574
[Notifications API] isTeacher=false, isStudent=true
[Notifications API] Filtering by types: ['assignment', 'reminder', 'appreciation', 'encouragement', 'achievement']
[Notifications API] Student student-1767970006574 has 14 notifications
[Notifications API] First notification: { type: 'encouragement', title: 'Message from Your Teacher' }
```

## Outcome

- Impact: Fixed notification isolation between teacher/student roles, instant popup delivery working
- Tests: Manual verification - teacher sent note, student received popup within 1-2 seconds
- Files: 7 files changed (3 API routes, 1 HTML, 3 skill files)
- Next prompts: Consider WebSocket for true real-time instead of polling
- Reflection: Role-based filtering at API level + visual debugging indicators greatly simplified troubleshooting

## Evaluation notes (flywheel)

- Failure modes observed: Initial confusion about which user was logged in; solved by adding visual user ID indicator
- Graders run and results (PASS/FAIL): PASS - Manual test confirmed student receives correct notifications
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Reduce polling to WebSocket for zero-latency notifications
