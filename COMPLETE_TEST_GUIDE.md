# Complete Frontend + Backend Testing Guide

## Quick Start - Minimum Requirements

### **Required Keys (Only 1 Needed!)**
```bash
# .env file - Just add this ONE key:
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx
```

That's it! Everything else works without external services for testing.

---

## Testing Strategy: 3 Approaches

### **Approach 1: Full Local (Recommended for Testing) ⭐**

**What you need:**
- ✅ Anthropic API key (for Claude)
- ✅ Local Python environment
- ✅ Node.js installed
- ❌ No Kafka needed (in-memory fallback)
- ❌ No PostgreSQL needed (in-memory fallback)
- ❌ No Docker needed

**Time to setup:** 5 minutes
**Cost:** Free (Anthropic free tier)

```bash
# 1. Set API key
echo "ANTHROPIC_API_KEY=sk-ant-your-key-here" > .env

# 2. Start all 6 backend agents
start-agents.bat

# 3. Start frontend
cd mystery-skils-app-ui
npm run dev

# 4. Open browser
# http://localhost:4000/mystery-skills-flash.html
```

**What works:**
- ✅ All 6 agents (using in-memory storage)
- ✅ Flash UI mastery display
- ✅ Real Claude API responses
- ✅ Progress tracking (in-memory)
- ❌ No persistence (resets on restart)
- ❌ No auth (anyone can access)

---

### **Approach 2: With Persistence (Better for Demo)**

**Additional requirements:**
- ✅ Supabase account (free tier)
- ✅ Better-Auth setup
- ❌ Still no Kafka/Docker needed

**Time to setup:** 15 minutes
**Cost:** Free

#### Step-by-Step:

**1. Get Supabase Database (2 minutes)**

```bash
# Sign up: https://supabase.com
# Create new project
# Copy connection string

# Add to .env:
DATABASE_URL=postgresql://postgres:[password]@db.xxx.supabase.co:5432/postgres
```

**2. Setup Better-Auth (5 minutes)**

```bash
cd mystery-skils-app-ui

# Install dependencies
npm install better-auth @better-auth/react prisma @prisma/client

# Initialize Prisma
npx prisma generate
npx prisma db push

# Add to .env:
BETTER_AUTH_SECRET=$(openssl rand -base64 32)
NEXT_PUBLIC_APP_URL=http://localhost:4000
```

**3. Start Everything**

```bash
# Terminal 1: Backend agents
cd D:\reuse-skills
start-agents.bat

# Terminal 2: Frontend
cd mystery-skils-app-ui
npm run dev
```

**What works:**
- ✅ Everything from Approach 1
- ✅ User authentication (Student/Teacher)
- ✅ Progress persistence (survives restart)
- ✅ Multi-user support
- ✅ Role-based access

---

### **Approach 3: Full Production Setup (Overkill for Testing)**

**Additional requirements:**
- Confluent Cloud / Upstash Kafka
- Production database
- Docker containers

**Time:** 1+ hour
**Cost:** May require paid tiers
**Recommendation:** Only use for final deployment

---

## Complete Testing Checklist

### **Phase 1: Backend Verification (5 min)**

```bash
# Check all agents are running
curl http://localhost:8001/health  # Triage
curl http://localhost:8002/health  # Concepts
curl http://localhost:8003/health  # Code Review
curl http://localhost:8004/health  # Debug
curl http://localhost:8005/health  # Exercise
curl http://localhost:8006/health  # Progress

# Expected: All return {"status":"healthy"}
```

### **Phase 2: Individual Agent Testing (10 min)**

#### 1. **Triage Agent** (Query Routing)
```bash
curl -X POST http://localhost:8001/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "query_id": "test-001",
    "student_id": "demo-student-001",
    "query_text": "What is a variable?",
    "code_snippet": null
  }'

# Expected: routing decision with detected_intent: "concept_explanation"
```

#### 2. **Concepts Agent** (Explanations)
```bash
curl -X POST http://localhost:8002/api/v1/explain \
  -H "Content-Type: application/json" \
  -d '{
    "query_id": "test-002",
    "student_id": "demo-student-001",
    "concept": "recursion",
    "difficulty_level": "beginner"
  }'

# Expected: JSON with explanation, code_examples, key_points
```

#### 3. **Code Review Agent**
```bash
curl -X POST http://localhost:8003/api/v1/review \
  -H "Content-Type: application/json" \
  -d '{
    "query_id": "test-003",
    "student_id": "demo-student-001",
    "code": "def add(a,b):\n  return a+b",
    "language": "python",
    "context": "Simple addition function"
  }'

# Expected: feedback_items, overall_rating, strengths, improvements
```

#### 4. **Debug Agent**
```bash
curl -X POST http://localhost:8004/api/v1/diagnose \
  -H "Content-Type: application/json" \
  -d '{
    "query_id": "test-004",
    "student_id": "demo-student-001",
    "error_message": "NameError: name x is not defined",
    "code_snippet": "print(x)",
    "error_type": "runtime"
  }'

# Expected: root_cause_analysis, error_classification, suggested_fixes
```

#### 5. **Exercise Generator**
```bash
curl -X POST http://localhost:8005/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "query_id": "test-005",
    "student_id": "demo-student-001",
    "topic": "loops",
    "difficulty": "beginner",
    "count": 3
  }'

# Expected: exercises array with problem_statement, starter_code, test_cases
```

#### 6. **Progress Tracker**
```bash
# Get mastery data (already tested)
curl http://localhost:8006/api/v1/mastery/demo-student-001

# Update mastery
curl -X POST http://localhost:8006/api/v1/mastery/demo-student-001 \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "demo-student-001",
    "topic": "functions",
    "interaction_type": "success",
    "success": true
  }'

# Expected: Updated mastery_percentage
```

### **Phase 3: Frontend Testing (10 min)**

#### Test Sequence:

**1. Landing Page**
```
URL: http://localhost:4000/mystery-skills-flash.html
Test:
- 3D neural mesh animation loads
- "BEGIN LEARNING" button visible
- Click → transitions to Auth page
```

**2. Auth Page** (if implemented)
```
Test:
- Role toggle (Student/Teacher) works
- Enter: test@student.com / password123
- Terminal shows authentication logs
- Redirects to dashboard on success
```

**3. Dashboard**
```
Test:
- Backend status shows "OPERATIONAL" (green)
- Global mastery displays (56%)
- 4 topic bars show with colors:
  - Variables: 100% (green)
  - Control Flow: 65% (yellow)
  - Data Structures: 30% (red)
  - Functions: 30% (red)
- Console shows topic names and percentages
- 3D mastery sphere rotates
```

**4. Agent Integration**
```
Test Flow:
1. Submit question via Triage Agent (if chat interface exists)
2. Watch terminal logs for routing decision
3. See response appear
4. Check Progress Tracker updates mastery
5. Dashboard reflects new mastery level
```

### **Phase 4: End-to-End Flow (5 min)**

**Complete User Journey:**

```bash
# Scenario: Student learns about variables

# 1. Student asks question
curl -X POST http://localhost:8001/api/v1/analyze \
  -d '{"query_id":"flow-001","student_id":"test-student","query_text":"What is a variable?"}'

# 2. Triage routes to Concepts Agent
# (happens automatically via Kafka or you can call directly)

# 3. Get explanation
curl -X POST http://localhost:8002/api/v1/explain \
  -d '{"query_id":"flow-001","student_id":"test-student","concept":"variables"}'

# 4. Update progress
curl -X POST http://localhost:8006/api/v1/mastery/test-student \
  -d '{"student_id":"test-student","topic":"variables","interaction_type":"success","success":true}'

# 5. Check updated mastery in UI
# Refresh dashboard → see variables mastery increase
```

---

## Environment Variables Reference

### **Minimal Setup (.env)**
```bash
# Required
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Optional (for full features)
DATABASE_URL=postgresql://localhost:5432/learnflow
BETTER_AUTH_SECRET=your-32-char-secret
NEXT_PUBLIC_APP_URL=http://localhost:4000

# Agent Ports (defaults)
TRIAGE_PORT=8001
CONCEPTS_PORT=8002
CODE_REVIEW_PORT=8003
DEBUG_PORT=8004
EXERCISE_PORT=8005
PROGRESS_PORT=8006
```

### **With External Services (.env.production)**
```bash
# Claude API
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Supabase Database
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres

# Better-Auth
BETTER_AUTH_SECRET=xxx
BETTER_AUTH_URL=https://your-domain.com

# Upstash Kafka (if using)
UPSTASH_KAFKA_REST_URL=https://xxxxx.upstash.io
UPSTASH_KAFKA_REST_USERNAME=xxxxx
UPSTASH_KAFKA_REST_PASSWORD=xxxxx

# Frontend URL
NEXT_PUBLIC_API_URL=https://your-domain.com
NEXT_PUBLIC_APP_URL=https://your-domain.com
```

---

## Quick Test Scripts

### **Test All Agents (Windows)**
```bat
@echo off
echo Testing all LearnFlow agents...

echo.
echo [1/6] Testing Triage Agent...
curl -s http://localhost:8001/health

echo.
echo [2/6] Testing Concepts Agent...
curl -s http://localhost:8002/health

echo.
echo [3/6] Testing Code Review Agent...
curl -s http://localhost:8003/health

echo.
echo [4/6] Testing Debug Agent...
curl -s http://localhost:8004/health

echo.
echo [5/6] Testing Exercise Agent...
curl -s http://localhost:8005/health

echo.
echo [6/6] Testing Progress Agent...
curl -s http://localhost:8006/health

echo.
echo All tests complete!
pause
```

Save as `test-all-agents.bat` and run.

### **Generate Test Data (Python)**
```python
# generate-test-data.py
import requests
import time

BASE_URL = "http://localhost:8006/api/v1"
STUDENT_ID = "demo-student-001"

topics = [
    ("variables-and-data-types", 10, 1),  # 90% success
    ("control-flow", 8, 2),                # 80% success
    ("data-structures", 4, 6),             # 40% success
    ("functions", 5, 5),                   # 50% success
]

for topic, successes, failures in topics:
    print(f"\nGenerating data for {topic}...")

    # Successful interactions
    for i in range(successes):
        response = requests.post(
            f"{BASE_URL}/mastery/{STUDENT_ID}",
            json={
                "student_id": STUDENT_ID,
                "topic": topic,
                "interaction_type": "success",
                "success": True
            }
        )
        print(f"  ✓ Success {i+1}/{successes}")
        time.sleep(0.1)

    # Failed interactions
    for i in range(failures):
        response = requests.post(
            f"{BASE_URL}/mastery/{STUDENT_ID}",
            json={
                "student_id": STUDENT_ID,
                "topic": topic,
                "interaction_type": "error",
                "success": False
            }
        )
        print(f"  ✗ Failure {i+1}/{failures}")
        time.sleep(0.1)

# Get final mastery
response = requests.get(f"{BASE_URL}/mastery/{STUDENT_ID}")
data = response.json()

print("\n" + "="*50)
print(f"Overall Mastery: {data['overall_mastery']*100:.1f}%")
print("="*50)

for topic in data['topic_mastery']:
    print(f"{topic['topic_name']}: {topic['mastery_percentage']:.1f}%")
```

Run: `python generate-test-data.py`

---

## Troubleshooting

### **Backend agents not starting**
```bash
# Check Python version
python --version  # Should be 3.11+

# Install dependencies
pip install -r backend/requirements.txt

# Start individually
python -m backend.agents.triage.main
```

### **Frontend not loading**
```bash
# Check Node version
node --version  # Should be 18+

# Clear cache and reinstall
cd mystery-skils-app-ui
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### **Mastery data not showing**
```bash
# Verify Progress Agent is running
curl http://localhost:8006/health

# Check if test data exists
curl http://localhost:8006/api/v1/mastery/demo-student-001

# If not, create test data:
python generate-test-data.py
```

### **CORS errors in browser**
- Check that all agents have CORS enabled (they should by default)
- Verify frontend is accessing http://localhost:XXXX (not 127.0.0.1)

---

## **Recommended Testing Flow**

**For quickest demo (10 minutes):**

1. ✅ **Get Anthropic API key** (free tier)
2. ✅ **Add to .env file**
3. ✅ **Run `start-agents.bat`**
4. ✅ **Run `npm run dev` in mystery-skils-app-ui**
5. ✅ **Open http://localhost:4000/mystery-skills-flash.html**
6. ✅ **Test dashboard shows mastery data**
7. ✅ **Test individual agents with curl**

**For complete demo with auth (30 minutes):**

1. Do steps 1-3 above
2. ✅ **Setup Supabase** (free)
3. ✅ **Install Better-Auth**
4. ✅ **Create auth page**
5. ✅ **Test login/signup**
6. ✅ **Test student vs teacher dashboards**

**Best approach:** Start with Approach 1 (full local), get everything working, then add persistence (Approach 2) if needed for demos.
