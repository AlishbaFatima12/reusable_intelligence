# LearnFlow Dashboard Debugger Skill

You are a specialized debugger for the LearnFlow teacher/student dashboard system. Your mission is to quickly identify and fix common issues from authentication to dashboard functionality with minimal token expense.

## Project Architecture

### Frontend (Port 4000)
- **Main File**: `mystery-skils-app-ui/public/mystery-skills-flash.html`
- **Auth Pages**: Landing → Auth → Dashboard (role-based)
- **Tech**: Vanilla JavaScript, CSS, LocalStorage for session

### Backend Agents (FastAPI)
| Agent | Port | Endpoint | Purpose |
|-------|------|----------|---------|
| Triage | 8001 | `/triage/classify` | Query classification |
| Concepts | 8002 | `/concepts/explain` | Concept explanations |
| Code Review | 8003 | `/api/v1/review` | Code review |
| Debug | 8004 | `/api/v1/debug` | Debugging help |
| Exercise | 8005 | `/api/v1/generate` | Generate exercises |
| Progress | 8006 | `/progress/{student_id}` | Track mastery |

### Next.js API Routes (Port 4000)
| Route | Purpose |
|-------|---------|
| `/api/auth/[...nextauth]` | Authentication |
| `/api/assignments/*` | Assignment CRUD |
| `/api/notifications/[userId]` | Notifications |

## Quick Diagnostic Commands

### Check Backend Health
```bash
curl http://localhost:8001/health  # Triage
curl http://localhost:8002/health  # Concepts
curl http://localhost:8005/health  # Exercise
curl http://localhost:8006/health  # Progress
```

### Check Frontend
```bash
curl http://localhost:4000/mystery-skills-flash.html
```

---

## ISSUE PATTERNS & FIXES

### 1. Authentication Issues

#### Problem: Auth buttons not clickable
**Symptom**: Login/Register buttons don't respond
**Cause**: Z-index or function not globally accessible
**Fix Location**: `mystery-skills-flash.html` - Function declarations
```javascript
// After function definition, add global export
window.toggleAuthMode = toggleAuthMode;
window.startHandshake = startHandshake;
window.togglePasswordVisibility = togglePasswordVisibility;
```

#### Problem: Password visibility toggle fails
**Symptom**: Eye icon click does nothing
**Fix**: Ensure onclick uses global function
```html
<span class="password-toggle" onclick="window.togglePasswordVisibility()">👁️</span>
```

---

### 2. Role-Based UI Issues

#### Problem: Student panel appears on teacher dashboard
**Symptom**: "YOUR_ASSIGNMENTS" panel shows for teachers
**Cause**: Missing role check in displayStudentAssignments
**Fix Location**: `mystery-skills-flash.html`
```javascript
function displayStudentAssignments(assignments) {
    const userStr = localStorage.getItem('learnflow_user');
    if (userStr) {
        const user = JSON.parse(userStr);
        if (user.role === 'teacher') {
            console.log('Skipping student assignments panel for teacher');
            return;  // Exit early for teachers
        }
    }
    // ... rest of function
}
```

#### Problem: Teacher sees student notifications
**Symptom**: Task assignments appear in teacher notification bell
**Cause**: API not filtering by role AND userId
**Fix Location**: `app/api/notifications/[userId]/route.ts`
```typescript
if (isTeacher) {
    notifications = await prisma.notification.findMany({
        where: {
            AND: [
                { userId: userId },  // Must match this teacher
                { type: { in: ['completion', 'confirmation'] } }
            ]
        },
        orderBy: { createdAt: 'desc' }
    })
}
```

#### Problem: Action buttons not appearing for teacher
**Symptom**: No SEND REMINDER, REGENERATE, SEND NOTE buttons
**Cause**: JavaScript syntax error or function not called
**Debug**:
1. Check browser console for errors
2. Search for `showStudentDetail` function
3. Verify button HTML generation has proper quote escaping

**Fix Pattern**:
```javascript
const html = `
    <button onclick="window.sendReminder('${studentId}')">SEND REMINDER</button>
    <button onclick="window.regenerateExercise('${studentId}')">REGENERATE</button>
    <button onclick="window.sendNote('${studentId}')">SEND NOTE</button>
`;
```

---

### 3. Page Navigation Issues

#### Problem: Landing page not visible on load (black screen)
**Symptom**: Must scroll to see content
**Cause**: CSS positioning issue
**Fix Location**: `mystery-skills-flash.html` - CSS section
```css
.page {
    display: none;
    position: fixed;  /* Changed from relative/absolute */
    top: 0;
    left: 0;
    width: 100%;
    min-height: 100vh;
    padding: 2rem;
    opacity: 0;
    transition: opacity 0.5s ease-in-out;
    overflow-y: auto;
    z-index: 10;
}
.page.active {
    display: block;
    opacity: 1;
    z-index: 20;
}
```

#### Problem: Page content stacks instead of overlaying
**Symptom**: Previous page visible behind current page
**Fix**: Same as above - use `position: fixed`

#### Problem: showPage not defined
**Symptom**: Console error "showPage is not defined"
**Fix**: Add global export
```javascript
window.showPage = showPage;
```

---

### 4. Notification Issues

#### Problem: Notifications not appearing in real-time
**Symptom**: Student doesn't see teacher notes immediately
**Cause**: Polling interval too long or first-load skip
**Fix Location**: `mystery-skills-flash.html`
```javascript
// Reduce polling interval
setInterval(async () => {
    await loadNotifications();
}, 3000);  // 3 seconds instead of 10

// Show popup for new notifications
function displayNotifications(notifications) {
    notifications.forEach(n => {
        if (!n.read && !displayedNotificationIds.has(n.id)) {
            displayedNotificationIds.add(n.id);
            showToast(n.title, n.message, 'info', 5000);
        }
    });
}
```

#### Problem: Teacher notification popup appears on wrong dashboard
**Symptom**: Notes sent to student popup on teacher's screen
**Cause**: Notification created with wrong userId
**Fix Location**: Assignment/notification creation API
```typescript
// When teacher sends to student, use STUDENT's userId
await prisma.notification.create({
    data: {
        userId: studentId,  // NOT teacherId
        type: 'assignment',
        title: 'New Task',
        message: messageContent
    }
})
```

---

### 5. Exercise Generation Issues

#### Problem: "Failed to fetch" or 404 on exercise generation
**Symptom**: REGENERATE button shows error
**Debug Steps**:
1. Check port: Exercise agent runs on **8005** (not 8003)
2. Check endpoint: `/api/v1/generate` (not `/generate`)
3. Check agent is running: `curl http://localhost:8005/health`

**Fix Location**: JavaScript fetch call
```javascript
const response = await fetch('http://localhost:8005/api/v1/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        query_id: `regen-${Date.now()}`,
        topic: 'python-basics',
        difficulty: 'beginner',
        count: 5
    })
});
```

#### Problem: Pydantic validation error in generator
**Symptom**: Exercises return empty, logs show "Input should be a valid string"
**Cause**: OpenAI returns list/int instead of string for test cases
**Fix Location**: `backend/agents/exercise/services/generator.py`
```python
for tc in ex_data["test_cases"]:
    tc_input = tc.get("input", "")
    tc_output = tc.get("expected_output", "")
    # Convert lists/ints to strings
    if isinstance(tc_input, list):
        tc_input = str(tc_input)
    if isinstance(tc_output, (list, int)):
        tc_output = str(tc_output)
    test_cases.append(TestCase(
        input=str(tc_input) if tc_input else "",
        expected_output=str(tc_output) if tc_output else "",
        explanation=tc.get("explanation")
    ))
```

---

### 6. Center Panel Issues

#### Problem: Selected student detail disappears during polling
**Symptom**: When viewing a student, panel reverts to class overview
**Cause**: `loadTeacherStats()` overwrites center panel during interval
**Fix Location**: `mystery-skills-flash.html`
```javascript
async function loadTeacherStats() {
    // Skip update if viewing specific student
    if (selectedStudentId) {
        return;
    }
    // ... rest of stats update
}
```

---

### 7. Form Validation Issues

#### Problem: Reminder sent without date
**Symptom**: Empty date submitted
**Fix**: Validate before sending
```javascript
function sendReminder(studentId) {
    const dueDate = document.getElementById('reminder-date').value;
    if (!dueDate) {
        showToast('⚠️ Date Required', 'Please select a due date', 'error', 3000);
        document.getElementById('reminder-date').style.borderColor = '#ff3131';
        document.getElementById('reminder-date').focus();
        return;
    }
    // Proceed with send
}
```

---

## TOKEN-EFFICIENT DEBUGGING WORKFLOW

### Step 1: Identify Issue Category
Read browser console first - most issues fall into:
- `not defined` → Global export missing
- `404` → Wrong endpoint/port
- Visual → CSS positioning
- Wrong data → API query filter

### Step 2: Targeted File Read
Only read the relevant section:
```javascript
// For button issues, search for the button generator
Grep: "SEND REMINDER"

// For notification issues
Read: app/api/notifications/[userId]/route.ts

// For role issues
Grep: "user.role"
```

### Step 3: Minimal Fix
Make the smallest change that fixes the issue. Common patterns:
- Add `window.functionName = functionName;` for onclick issues
- Add role check at function start for visibility issues
- Fix port number for API issues
- Add type conversion for Pydantic errors

### Step 4: Verify
```bash
# Quick health check
curl http://localhost:8005/health

# Or browser console
console.log(window.showPage);  // Should be function
```

---

## CRITICAL FILES REFERENCE

| File | Common Issues |
|------|---------------|
| `mystery-skills-flash.html` | Button clicks, page navigation, role checks, polling |
| `app/api/notifications/[userId]/route.ts` | Teacher/student notification filtering |
| `backend/agents/exercise/services/generator.py` | Pydantic validation, test case parsing |
| `prisma/schema.prisma` | Notification model, User model |

---

## VERSION TRACKING

Add version indicator to track deployments:
```html
<div style="position: fixed; bottom: 5px; left: 5px; font-size: 10px; color: rgba(255,255,255,0.3);">
    v1.2.7-role-fix
</div>
```

---

## DEBUGGING CHECKLIST

- [ ] Browser console clear of errors?
- [ ] All backend agents responding to /health?
- [ ] LocalStorage has correct user role?
- [ ] Global functions exported to window?
- [ ] CSS pages using position: fixed?
- [ ] Notification API filtering by userId AND type for teachers?
- [ ] Exercise generator converting lists to strings?
- [ ] Polling not overwriting selected student view?

---

## OUTPUT FORMAT

When reporting fixes:
1. **Issue**: One-line description
2. **Cause**: Root cause identified
3. **File**: `path/to/file.ext:line_number`
4. **Fix**: Code change applied
5. **Verified**: How it was tested

Example:
```
Issue: Student panel shows on teacher dashboard
Cause: Missing role check in displayStudentAssignments
File: mystery-skills-flash.html:2593
Fix: Added early return for teacher role
Verified: Teacher login shows no "YOUR_ASSIGNMENTS" panel
```
