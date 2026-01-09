# LearnFlow Quick Fix Reference

## Most Common Issues (Copy-Paste Fixes)

### 1. Function Not Defined Error
Add after function declaration:
```javascript
window.showPage = showPage;
window.toggleAuthMode = toggleAuthMode;
window.startHandshake = startHandshake;
window.logout = logout;
window.refreshTeacherData = refreshTeacherData;
```

### 2. Wrong Panel for Role
Add at function start:
```javascript
const user = JSON.parse(localStorage.getItem('learnflow_user') || '{}');
if (user.role === 'teacher') return;  // Skip for teachers
```

### 3. Exercise 404 Error
Fix endpoint:
```
Port: 8005 (NOT 8003)
Path: /api/v1/generate (NOT /generate)
```

### 4. Page Not Showing
Fix CSS:
```css
.page { position: fixed; top: 0; left: 0; }
```

### 5. Notification to Wrong User
Fix API query:
```typescript
where: {
  AND: [
    { userId: userId },
    { type: { in: ['completion', 'confirmation'] } }
  ]
}
```

### 6. Test Case Validation Error
Fix in generator.py:
```python
tc_input = str(tc.get("input", "")) if tc.get("input") else ""
tc_output = str(tc.get("expected_output", "")) if tc.get("expected_output") else ""
```

### 7. Center Panel Disappears
Add check in loadTeacherStats:
```javascript
if (selectedStudentId) return;  // Don't overwrite student view
```

### 8. Date Validation
```javascript
if (!dueDate) {
    showToast('Date Required', 'Select date first', 'error');
    return;
}
```

## Agent Ports Quick Reference
| Agent | Port | Health Check |
|-------|------|--------------|
| Triage | 8001 | `curl localhost:8001/health` |
| Concepts | 8002 | `curl localhost:8002/health` |
| Code Review | 8003 | `curl localhost:8003/health` |
| Debug | 8004 | `curl localhost:8004/health` |
| Exercise | 8005 | `curl localhost:8005/health` |
| Progress | 8006 | `curl localhost:8006/health` |
| Frontend | 4000 | `curl localhost:4000` |
