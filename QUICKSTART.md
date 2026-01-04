# LearnFlow - Quick Start (No Docker)

Lightweight setup for testing backend agents without Docker infrastructure.

---

## ✅ What Works Without Docker

**Backend Agents**:
- ✅ All 3 agents start and run independently
- ✅ Health checks work (`/health`, `/ready`)
- ✅ API endpoints work (direct HTTP calls)
- ✅ Claude API integration works (if you have API key)
- ✅ Prometheus metrics work

**What Doesn't Work (Yet)**:
- ❌ Kafka messaging (agents won't communicate between each other)
- ❌ PostgreSQL state persistence (Progress Tracker won't save data)
- ❌ WebSocket Bridge (requires Kafka)
- ❌ Real-time frontend updates (requires WebSocket)

**Frontend UI**:
- ✅ UI starts and displays
- ✅ Can call backend APIs directly
- ⚠️ Real-time updates won't work (no WebSocket)

---

## 🚀 Step-by-Step Setup

### 1. Create Python Virtual Environment

```bash
# Navigate to project root
cd D:\reuse-skills

# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# You should see (venv) in your prompt now
```

### 2. Install Backend Dependencies

```bash
# Install shared dependencies
pip install -r backend/requirements.txt

# This installs:
# - FastAPI, Uvicorn (web framework)
# - Anthropic SDK (Claude API)
# - Pydantic (data validation)
# - And more...
```

### 3. Set Your API Key

```bash
# Create .env file in project root
copy .env.example .env

# Edit .env and add your Anthropic API key
# Use notepad or any text editor:
notepad .env
```

**In .env file**, set:
```env
ANTHROPIC_API_KEY=your-actual-api-key-here
CLAUDE_MODEL=claude-sonnet-3-5-20241022
```

---

## 🎯 Start Backend Agents

Open **3 separate PowerShell/CMD windows** and run these commands:

### Terminal 1: Triage Agent (Port 8001)

```bash
cd D:\reuse-skills
venv\Scripts\activate
cd backend\agents\triage
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

**Expected output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Terminal 2: Concepts Agent (Port 8002)

```bash
cd D:\reuse-skills
venv\Scripts\activate
cd backend\agents\concepts
uvicorn main:app --host 0.0.0.0 --port 8002 --reload
```

### Terminal 3: Progress Tracker (Port 8006)

```bash
cd D:\reuse-skills
venv\Scripts\activate
cd backend\agents\progress
uvicorn main:app --host 0.0.0.0 --port 8006 --reload
```

---

## 🧪 Test Each Agent

### Test 1: Health Checks

Open a **new terminal** and test:

```bash
# Triage Agent
curl http://localhost:8001/health

# Concepts Agent
curl http://localhost:8002/health

# Progress Tracker
curl http://localhost:8006/health
```

**Expected**: `{"status":"healthy","uptime_seconds":...}`

### Test 2: Triage Agent - Classify Query

```bash
curl -X POST http://localhost:8001/api/v1/analyze -H "Content-Type: application/json" -d "{\"query_id\":\"test-001\",\"student_id\":\"student-123\",\"query_text\":\"What is recursion?\"}"
```

**Expected**: JSON response with `detected_intent`, `confidence_score`, `routed_to_agent`

### Test 3: Concepts Agent - Generate Explanation

```bash
curl -X POST http://localhost:8002/api/v1/explain -H "Content-Type: application/json" -d "{\"query_id\":\"test-002\",\"student_id\":\"student-123\",\"concept\":\"recursion\",\"difficulty_level\":\"beginner\",\"include_examples\":true}"
```

**Expected**: Detailed explanation with code examples (uses Claude API)

### Test 4: Progress Tracker - Get Mastery

```bash
# Get current mastery (will create new student if not exists)
curl http://localhost:8006/api/v1/mastery/student-123

# Update mastery
curl -X POST http://localhost:8006/api/v1/mastery/student-123 -H "Content-Type: application/json" -d "{\"student_id\":\"student-123\",\"topic\":\"recursion\",\"interaction_type\":\"success\",\"success\":true}"
```

**Expected**: Mastery response with topic breakdowns

---

## 🎨 Start Frontend (Optional)

If you want to see the UI:

```bash
# Open new terminal
cd D:\reuse-skills\mystery-skils-app-ui

# Install dependencies (first time only)
npm install

# Start dev server
npm run dev
```

Open browser: **http://localhost:4000**

**Note**: Real-time updates won't work without WebSocket Bridge (which requires Kafka). But you can still see the UI and manually refresh data.

---

## ⚠️ Troubleshooting

### "Module not found" errors

```bash
# Make sure venv is activated
# You should see (venv) in your prompt

# If not:
venv\Scripts\activate

# Reinstall dependencies
pip install -r backend/requirements.txt
```

### Port already in use

```bash
# Find process using port 8001 (example)
netstat -ano | findstr :8001

# Kill it
taskkill /PID <process_id> /F
```

### "ANTHROPIC_API_KEY not found"

```bash
# Check .env file exists in project root
dir .env

# Check it contains your key
type .env

# Make sure agents are reading it (they auto-load .env from parent directories)
```

### Agent crashes with Kafka error

This is **expected** without Docker! The agents try to connect to Kafka but gracefully handle the failure. The HTTP endpoints still work.

**To suppress warnings**, you can temporarily comment out Kafka publishing code, but it's not necessary - the agents will work for direct API testing.

---

## 📊 What's Working

With this setup, you can:

✅ **Test each agent independently** via HTTP endpoints
✅ **Verify Claude API integration** (Triage & Concepts use Claude)
✅ **Check health endpoints** and Prometheus metrics
✅ **See agent logs** in each terminal window
✅ **Test Progress Tracker** mastery calculation (won't persist without PostgreSQL)
✅ **Run frontend UI** (but no real-time updates)

---

## 🔄 Next Steps

### When you're ready for full integration:

1. **Start Docker Desktop**
2. Run `docker-compose up -d` (Kafka + PostgreSQL)
3. Start WebSocket Bridge: `cd backend\websocket-bridge && python main.py`
4. Now you get:
   - ✅ Agent-to-agent communication via Kafka
   - ✅ Data persistence in PostgreSQL
   - ✅ Real-time WebSocket updates in frontend

### Add remaining 3 agents:

After testing core 3 agents, implement:
- Code Review Agent (Port 8003)
- Debug Agent (Port 8004)
- Exercise Generator (Port 8005)

---

## 💡 Pro Tips

**Keep terminals organized**:
- Terminal 1: Triage (8001) - Routing
- Terminal 2: Concepts (8002) - Explanations
- Terminal 3: Progress (8006) - Analytics
- Terminal 4: Frontend (4000) - UI

**Watch the logs**: Each agent prints structured JSON logs. You'll see:
- Claude API calls
- Request processing
- Errors (if any)

**Test incrementally**: Start with just Triage, get it working, then add Concepts, then Progress.

---

## 🆘 Need Help?

If something doesn't work:
1. Check agent logs in the terminal
2. Verify `.env` file has your API key
3. Make sure venv is activated (`(venv)` in prompt)
4. Check ports aren't already in use

**All agents should start successfully even without Kafka/PostgreSQL!**
