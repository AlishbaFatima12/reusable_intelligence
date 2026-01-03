# LearnFlow Quick Start Guide

**Feature**: `002-learnflow-platform`
**Date**: 2026-01-02
**Prerequisites**: Docker, Docker Compose, Node.js 18+, Python 3.11+

## Overview

Get the LearnFlow Multi-Agent Learning Platform running locally in under 10 minutes. This guide covers:
1. Setting up the backend (6 FastAPI agents + Kafka + PostgreSQL + Dapr)
2. Starting the Mystery Skills UI frontend
3. Testing the full system end-to-end

---

## Architecture Quick Reference

```
┌─────────────────────────────────────────────────────────────┐
│                    Mystery Skills UI (Next.js)              │
│          3D Sphere | Hacker Terminal | Teacher HUD          │
│                   http://localhost:4000                     │
└───────────────────────┬─────────────────────────────────────┘
                        │ WebSocket + REST API
                        ▼
┌───────────────────────────────────────────────────────────┐
│  Triage Agent (8001) ──→ Kafka ──→ Specialist Agents      │
│  Concepts (8002)     Dapr State Store (PostgreSQL)         │
│  Code Review (8003)  Pub/Sub Topics (7 topics)             │
│  Debug (8004)        Claude API (Runtime LLM calls)        │
│  Exercise (8005)                                            │
│  Progress (8006)                                            │
└─────────────────────────────────────────────────────────────┘
```

---

## Step 1: Environment Setup

### 1.1 Create .env File

Create `.env` in the repository root:

```bash
# Claude API Configuration
ANTHROPIC_API_KEY=your-claude-api-key-here
CLAUDE_MODEL=claude-sonnet-3-5-20241022

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS=localhost:9092

# PostgreSQL Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=learnflow
POSTGRES_USER=learnflow_user
POSTGRES_PASSWORD=learnflow_password

# Dapr Configuration
DAPR_HTTP_PORT=3500
DAPR_GRPC_PORT=50001

# Agent Ports
TRIAGE_PORT=8001
CONCEPTS_PORT=8002
CODE_REVIEW_PORT=8003
DEBUG_PORT=8004
EXERCISE_PORT=8005
PROGRESS_PORT=8006

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_SOCKET_URL=http://localhost:8081
```

**Get Claude API Key**: Visit https://console.anthropic.com/settings/keys

---

## Step 2: Start Infrastructure (Kafka, PostgreSQL, Dapr)

### 2.1 Start with Docker Compose

```bash
# Start Kafka, Zookeeper, PostgreSQL
docker-compose up -d kafka zookeeper postgres

# Wait for services to be ready (30 seconds)
sleep 30

# Verify Kafka is running
docker-compose ps
```

### 2.2 Initialize Dapr

```bash
# Install Dapr CLI (if not already installed)
wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash

# Initialize Dapr (local mode)
dapr init

# Verify Dapr installation
dapr --version
```

### 2.3 Create Kafka Topics

```bash
# Create all required topics
docker exec -it learnflow-kafka kafka-topics.sh \
  --create --bootstrap-server localhost:9092 \
  --topic student-queries --partitions 6 --replication-factor 1

docker exec -it learnflow-kafka kafka-topics.sh \
  --create --bootstrap-server localhost:9092 \
  --topic triage-routing --partitions 6 --replication-factor 1

docker exec -it learnflow-kafka kafka-topics.sh \
  --create --bootstrap-server localhost:9092 \
  --topic agent-responses --partitions 6 --replication-factor 1

docker exec -it learnflow-kafka kafka-topics.sh \
  --create --bootstrap-server localhost:9092 \
  --topic student-struggle --partitions 3 --replication-factor 1

docker exec -it learnflow-kafka kafka-topics.sh \
  --create --bootstrap-server localhost:9092 \
  --topic mastery-updates --partitions 6 --replication-factor 1

docker exec -it learnflow-kafka kafka-topics.sh \
  --create --bootstrap-server localhost:9092 \
  --topic agent-logs --partitions 6 --replication-factor 1

docker exec -it learnflow-kafka kafka-topics.sh \
  --create --bootstrap-server localhost:9092 \
  --topic agent-status --partitions 1 --replication-factor 1

# Verify topics created
docker exec -it learnflow-kafka kafka-topics.sh \
  --list --bootstrap-server localhost:9092
```

---

## Step 3: Start Backend Agents

### 3.1 Install Python Dependencies

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3.2 Start Each Agent with Dapr

**Terminal 1: Triage Agent**
```bash
cd backend/agents/triage
dapr run --app-id triage --app-port 8001 --dapr-http-port 3501 \
  --components-path ../../../infrastructure/dapr/components \
  -- python main.py
```

**Terminal 2: Concepts Agent**
```bash
cd backend/agents/concepts
dapr run --app-id concepts --app-port 8002 --dapr-http-port 3502 \
  --components-path ../../../infrastructure/dapr/components \
  -- python main.py
```

**Terminal 3: Code Review Agent**
```bash
cd backend/agents/code-review
dapr run --app-id code-review --app-port 8003 --dapr-http-port 3503 \
  --components-path ../../../infrastructure/dapr/components \
  -- python main.py
```

**Terminal 4: Debug Agent**
```bash
cd backend/agents/debug
dapr run --app-id debug --app-port 8004 --dapr-http-port 3504 \
  --components-path ../../../infrastructure/dapr/components \
  -- python main.py
```

**Terminal 5: Exercise Generator**
```bash
cd backend/agents/exercise
dapr run --app-id exercise --app-port 8005 --dapr-http-port 3505 \
  --components-path ../../../infrastructure/dapr/components \
  -- python main.py
```

**Terminal 6: Progress Tracker**
```bash
cd backend/agents/progress
dapr run --app-id progress --app-port 8006 --dapr-http-port 3506 \
  --components-path ../../../infrastructure/dapr/components \
  -- python main.py
```

### 3.3 Verify Agents Are Running

```bash
# Check all agents are healthy
curl http://localhost:8001/health  # Triage
curl http://localhost:8002/health  # Concepts
curl http://localhost:8003/health  # Code Review
curl http://localhost:8004/health  # Debug
curl http://localhost:8005/health  # Exercise
curl http://localhost:8006/health  # Progress Tracker

# Expected response: {"status": "healthy"}
```

---

## Step 4: Start Frontend

### 4.1 Install Frontend Dependencies

```bash
cd mystery-skils-app-ui
npm install --legacy-peer-deps
```

### 4.2 Start Next.js Development Server

```bash
npm run dev
# Runs on http://localhost:4000
```

### 4.3 Open Browser

Visit: **http://localhost:4000**

You should see:
- **3D Mastery Sphere** (center) - All 7 Python topics at 0% (red rings)
- **Hacker Terminal** (right) - Real-time agent logs
- **Teacher HUD** (left) - Student monitoring (empty initially)
- **MYSTERY SKILLS** title (top center)

---

## Step 5: Test End-to-End

### 5.1 Submit a Test Query

**Option A: Via Chat Interface (Frontend)**
1. Type in chat: "What is recursion?"
2. Submit query

**Option B: Via Triage Agent API (cURL)**
```bash
curl -X POST http://localhost:8001/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "query_id": "test-001",
    "student_id": "student_123",
    "query_text": "Can you explain what recursion is with an example?"
  }'
```

### 5.2 Verify Query Flow

**Expected Flow**:
1. **Triage Agent** analyzes query → detects intent "concept" → routes to Concepts Agent
2. **Concepts Agent** receives request via Kafka → calls Claude API → generates explanation
3. **Response** published to `agent-responses` Kafka topic
4. **Frontend** receives response via WebSocket → displays in chat

**Check Logs**:
```bash
# Watch Kafka messages
docker exec -it learnflow-kafka kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic agent-logs \
  --from-beginning

# Expected log sequence:
# [TRIAGE] Analyzing query test-001
# [TRIAGE] Detected intent: concept, routing to concepts
# [CONCEPTS] Received query test-001
# [CONCEPTS] Calling Claude API for explanation
# [CONCEPTS] Response generated in 1200ms
```

### 5.3 Test Each Agent Type

**Concept Query** (Concepts Agent):
```bash
curl -X POST http://localhost:8001/analyze \
  -H "Content-Type: application/json" \
  -d '{"query_id": "q-001", "student_id": "s1", "query_text": "What is a list?"}'
```

**Code Review Query** (Code Review Agent):
```bash
curl -X POST http://localhost:8001/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "query_id": "q-002",
    "student_id": "s1",
    "query_text": "Review my code",
    "code_snippet": "def add(a, b):\n    result = a + b\n    return result"
  }'
```

**Debug Query** (Debug Agent):
```bash
curl -X POST http://localhost:8001/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "query_id": "q-003",
    "student_id": "s1",
    "query_text": "Why does this give IndexError?",
    "code_snippet": "my_list = [1, 2, 3]\nprint(my_list[5])"
  }'
```

**Exercise Request** (Exercise Generator):
```bash
curl -X POST http://localhost:8001/analyze \
  -H "Content-Type: application/json" \
  -d '{"query_id": "q-004", "student_id": "s1", "query_text": "Give me practice problems for loops"}'
```

**Progress Query** (Progress Tracker):
```bash
curl -X POST http://localhost:8001/analyze \
  -H "Content-Type: application/json" \
  -d '{"query_id": "q-005", "student_id": "s1", "query_text": "Show me my learning progress"}'
```

---

## Step 6: Verify Dashboard Updates

### 6.1 Check 3D Mastery Sphere

After completing exercises, mastery levels should update:
- **Red rings (0%)** → **Orange (33%)** → **Green (66%)** → **Blue (100%)**
- Progress Tracker publishes `mastery.level.updated` events to Kafka
- Frontend subscribes and updates sphere in real-time

### 6.2 Check Hacker Terminal

Terminal should show:
- Agent log entries from all 6 agents
- Color-coded by level: INFO (cyan), WARN (yellow), ERROR (red), SUCCESS (green)
- Auto-scrolling with latest logs at bottom

### 6.3 Check Teacher HUD

When struggle detected (5+ failed runs):
- Student card appears in left panel
- **Pulsing RED alert** icon
- Shows: failed run count, current topic, last activity

**Trigger Struggle Detection**:
```bash
# Fail 6 times on same topic
for i in {1..6}; do
  curl -X POST http://localhost:8006/struggle-detection \
    -H "Content-Type: application/json" \
    -d "{
      \"student_id\": \"student_123\",
      \"recent_queries\": [{\"query_id\": \"q-$i\", \"success\": false}]
    }"
done
```

---

## Common Issues & Troubleshooting

### Issue: "Connection refused" on port 8001

**Cause**: Triage Agent not running
**Fix**:
```bash
cd backend/agents/triage
dapr run --app-id triage --app-port 8001 -- python main.py
```

### Issue: "Claude API error: 401 Unauthorized"

**Cause**: Invalid ANTHROPIC_API_KEY
**Fix**: Verify `.env` has correct API key from https://console.anthropic.com/settings/keys

### Issue: "Kafka broker not available"

**Cause**: Kafka container not running
**Fix**:
```bash
docker-compose up -d kafka zookeeper
sleep 30  # Wait for startup
```

### Issue: "WebSocket connection failed"

**Cause**: WebSocket server not started
**Fix**: Ensure `mystery-skils-app-ui/app/api/socket/route.ts` is implemented and Next.js is running on port 4000

### Issue: "No mastery updates in UI"

**Cause**: Progress Tracker not publishing to Kafka
**Fix**:
1. Check Progress Tracker logs: `docker logs learnflow-progress`
2. Verify Kafka topic exists: `docker exec -it learnflow-kafka kafka-topics.sh --list --bootstrap-server localhost:9092`
3. Test Progress Tracker directly: `curl http://localhost:8006/mastery/student_123`

---

## Development Workflow

### Run Tests

```bash
# Backend unit tests
cd backend
pytest tests/unit -v

# Integration tests (requires Kafka + PostgreSQL running)
pytest tests/integration -v

# Frontend tests
cd mystery-skils-app-ui
npm test
```

### Watch Logs

```bash
# All Kafka topics
docker exec -it learnflow-kafka kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic agent-logs \
  --from-beginning

# PostgreSQL query logs
docker logs -f learnflow-postgres

# Dapr logs
dapr logs --app-id triage
```

### Reset Database

```bash
# Drop all tables and restart
docker-compose down -v
docker-compose up -d postgres
sleep 10
python backend/scripts/init-db.py
```

---

## Architecture Validation Checklist

After completing quickstart, verify:

- ✅ All 6 agents running on ports 8001-8006
- ✅ Kafka has 7 topics (student-queries, triage-routing, agent-responses, etc.)
- ✅ PostgreSQL has 5 tables (student_queries, agent_responses, students, learning_progress, exercises)
- ✅ Dapr sidecars running for each agent
- ✅ Frontend displays 3D Sphere, Terminal, HUD
- ✅ Query submitted via Triage → routed to specialist → response displayed
- ✅ Real-time logs streaming in Hacker Terminal
- ✅ Mastery levels update after query completion
- ✅ Struggle detection triggers alert in Teacher HUD

---

## Next Steps

1. **Add Authentication**: Implement BetterAuth in `mystery-skils-app-ui/app/api/auth/`
2. **Deploy to Kubernetes**: Follow `docs/deployment-guide.md`
3. **Add More Agents**: Extend with custom specialist agents
4. **Scale Horizontally**: Add more Kafka partitions and agent instances

**For Full Documentation**: See `specs/002-learnflow-platform/plan.md`, `data-model.md`, and `contracts/`

---

**Questions?** Check `history/prompts/002-learnflow-platform/` for Prompt History Records or create an ADR at `history/adr/` for architectural decisions.
