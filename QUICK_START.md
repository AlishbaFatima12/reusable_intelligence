# 🚀 LearnFlow Quick Start Guide

## Test Your System in 3 Steps (5 minutes)

### **Step 1: Get Anthropic API Key** (1 min)

If you don't have one:
1. Go to https://console.anthropic.com
2. Sign up (free tier available)
3. Create API key
4. Copy it

### **Step 2: Configure Environment** (1 min)

Create `.env` file in project root:

```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

That's it! No Kafka, no PostgreSQL, no Docker needed for testing.

### **Step 3: Start Everything** (3 min)

```bash
# Terminal 1: Start all 6 backend agents
start-agents.bat

# Terminal 2: Start frontend
cd mystery-skils-app-ui
npm run dev

# Terminal 3: Run tests
python test_complete_system.py
```

---

## ✅ What You Should See

### **Backend Agents (Terminal 1)**
```
Starting Triage Agent (8001)...
Starting Concepts Agent (8002)...
Starting Code Review Agent (8003)...
Starting Debug Agent (8004)...
Starting Exercise Agent (8005)...
Starting Progress Tracker (8006)...
✓ All agents starting...
```

### **Frontend (Terminal 2)**
```
- Local: http://localhost:4000
✓ Ready in 2.3s
```

### **Test Results (Terminal 3)**
```
Phase 1: Agent Health Checks
[✓] Triage Agent Health - Status: healthy
[✓] Concepts Agent Health - Status: healthy
[✓] Code Review Agent Health - Status: healthy
[✓] Debug Agent Health - Status: healthy
[✓] Exercise Agent Health - Status: healthy
[✓] Progress Agent Health - Status: healthy

Phase 2: Functional Tests
[✓] Query Analysis - Intent: concept_explanation, Confidence: 0.94
[✓] Concept Explanation - Has explanation: True, Examples: 3
[✓] Code Review - Rating: good, Feedback items: 4
[✓] Error Diagnosis - Error type: NameError, Has root cause: True
[✓] Exercise Generation - Generated: 2 exercises
[✓] Progress Tracking - Overall: 52.3%, Topics: 3

Total Tests: 12
Passed: 12
Failed: 0
Success Rate: 100.0%

🎉 All tests passed! System is fully operational.
```

---

## 🌐 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| **Flash UI** | http://localhost:4000/mystery-skills-flash.html | Main dashboard |
| **Triage** | http://localhost:8001 | Query routing |
| **Concepts** | http://localhost:8002 | Explanations |
| **Code Review** | http://localhost:8003 | Code analysis |
| **Debug** | http://localhost:8004 | Error diagnosis |
| **Exercise** | http://localhost:8005 | Practice problems |
| **Progress** | http://localhost:8006 | Mastery tracking |

---

## 🎯 Test the Dashboard

1. Open: http://localhost:4000/mystery-skills-flash.html
2. Click "BEGIN LEARNING"
3. You should see:
   - ✅ Backend Status: OPERATIONAL (green)
   - ✅ Global Mastery: 56%
   - ✅ 4 colored mastery bars
   - ✅ Topic breakdown in console

**Expected Dashboard:**
```
Backend Status: OPERATIONAL

56% Global Mastery

[████████████████████████] VARIABLES AND DATA TYPES: 100%
[████████████]            CONTROL FLOW: 65%
[██████]                  DATA STRUCTURES: 30%
[██████]                  FUNCTIONS: 30%
```

---

## 🧪 Manual API Tests

### Quick cURL Tests

```bash
# 1. Check agent health
curl http://localhost:8001/health

# 2. Ask a question (Triage)
curl -X POST http://localhost:8001/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "query_id": "test-001",
    "student_id": "demo-student",
    "query_text": "What is recursion?"
  }'

# 3. Get explanation (Concepts)
curl -X POST http://localhost:8002/api/v1/explain \
  -H "Content-Type: application/json" \
  -d '{
    "query_id": "test-002",
    "student_id": "demo-student",
    "concept": "recursion",
    "difficulty_level": "beginner"
  }'

# 4. Review code (Code Review)
curl -X POST http://localhost:8003/api/v1/review \
  -H "Content-Type: application/json" \
  -d '{
    "query_id": "test-003",
    "student_id": "demo-student",
    "code": "def factorial(n): return 1 if n == 0 else n * factorial(n-1)"
  }'

# 5. Debug error (Debug)
curl -X POST http://localhost:8004/api/v1/diagnose \
  -H "Content-Type: application/json" \
  -d '{
    "query_id": "test-004",
    "student_id": "demo-student",
    "error_message": "IndexError: list index out of range"
  }'

# 6. Generate exercises (Exercise)
curl -X POST http://localhost:8005/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "query_id": "test-005",
    "student_id": "demo-student",
    "topic": "loops",
    "count": 3
  }'

# 7. Check mastery (Progress)
curl http://localhost:8006/api/v1/mastery/demo-student-001
```

---

## ❓ Troubleshooting

### **Agents won't start**
```bash
# Check Python version
python --version  # Need 3.11+

# Reinstall dependencies
pip install -r backend/requirements.txt
```

### **Frontend won't load**
```bash
cd mystery-skils-app-ui

# Clear and reinstall
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### **No mastery data in dashboard**
```bash
# The test data should already exist, but if not:
python test_complete_system.py

# Or manually create:
curl -X POST http://localhost:8006/api/v1/mastery/demo-student-001 \
  -H "Content-Type: application/json" \
  -d '{"student_id":"demo-student-001","topic":"variables","interaction_type":"success","success":true}'
```

### **API calls failing**
- Make sure all 6 agents are running (check Terminal 1)
- Verify ports are not already in use
- Check `.env` file has ANTHROPIC_API_KEY

---

## 📊 Full System Test

Want to test everything at once?

```bash
# Run comprehensive test suite
python test_complete_system.py

# Or test all agent health
test-all-agents.bat
```

---

## 🎨 What's Working

✅ **All 6 Agents**
- Triage routing decisions
- Concepts explanations with code examples
- Code reviews with feedback
- Error diagnosis and fixes
- Exercise generation with difficulty scaling
- Progress tracking with mastery calculations

✅ **Flash UI**
- 3D neural mesh visualization
- Real-time mastery display
- Color-coded progress bars
- Terminal-style console output
- Agentic Brutalism 2025 design

✅ **Backend Integration**
- REST API endpoints
- In-memory storage (for testing)
- Claude API integration
- Metrics and health checks

---

## 🔑 Required Keys Summary

**For testing (minimal):**
- `ANTHROPIC_API_KEY` - Get from https://console.anthropic.com

**For full features (optional):**
- `DATABASE_URL` - Supabase/PostgreSQL (for persistence)
- `BETTER_AUTH_SECRET` - For authentication
- `KAFKA_BOOTSTRAP_SERVERS` - For event streaming (or use Upstash)

**Start with just Anthropic key. Everything else works without it!**

---

## 📚 Next Steps

Once everything is working:

1. **Add Authentication**
   - See `AUTH_IMPLEMENTATION_PLAN.md`
   - Setup Better-Auth for Student/Teacher login

2. **Add Persistence**
   - Setup Supabase (free)
   - Progress data survives restarts

3. **Deploy**
   - Frontend → Vercel
   - Backend → Railway/Render
   - Database → Supabase

4. **Full Guide**
   - See `COMPLETE_TEST_GUIDE.md` for detailed testing
   - See `SETUP_GUIDE.md` for production setup

---

## 🚀 You're Ready!

Your LearnFlow platform should now be fully operational. Open the dashboard and start exploring!

**Dashboard URL:** http://localhost:4000/mystery-skills-flash.html

Need help? Check the guides:
- `COMPLETE_TEST_GUIDE.md` - Comprehensive testing
- `SETUP_GUIDE.md` - Auth, Kafka, Docker setup
- `AUTH_IMPLEMENTATION_PLAN.md` - Authentication design
