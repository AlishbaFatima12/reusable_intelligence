# LearnFlow Platform - Deployment & Testing Guide

Complete guide to deploy and test the LearnFlow Multi-Agent Learning Platform with Mystery Skills UI.

---

## 🎯 System Overview

**Backend**: 3 FastAPI agents + 1 WebSocket bridge
**Frontend**: Next.js 15 Mystery Skills UI
**Infrastructure**: Kafka, PostgreSQL, Dapr

**Agents**:
- **Triage Agent** (Port 8001): Intent classification & query routing
- **Concepts Agent** (Port 8002): Programming concept explanations
- **Progress Tracker** (Port 8006): Student mastery tracking & analytics
- **WebSocket Bridge** (Port 4001): Kafka → Socket.io real-time streaming

---

## 📋 Prerequisites

### Required Software
```bash
# Python 3.11+
python --version

# Node.js 18+
node --version
npm --version

# Docker & Docker Compose
docker --version
docker-compose --version
```

### Environment Setup
```bash
# 1. Copy environment template
cp .env.example .env

# 2. Add your Anthropic API key
# Edit .env and set:
ANTHROPIC_API_KEY=your-actual-api-key-here
```

---

## 🚀 Quick Start (Local Development)

### Step 1: Start Infrastructure

```bash
# Start Kafka, Zookeeper, PostgreSQL
docker-compose up -d

# Verify services are running
docker-compose ps

# Expected output:
#   kafka         Up      9092/tcp, 9093/tcp
#   postgres      Up      5432/tcp
#   zookeeper     Up      2181/tcp
```

### Step 2: Install Backend Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

### Step 3: Start Backend Agents

Open **4 separate terminals** and run:

**Terminal 1 - Triage Agent**:
```bash
cd backend/agents/triage
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 2 - Concepts Agent**:
```bash
cd backend/agents/concepts
uvicorn main:app --host 0.0.0.0 --port 8002 --reload
```

**Terminal 3 - Progress Tracker**:
```bash
cd backend/agents/progress
uvicorn main:app --host 0.0.0.0 --port 8006 --reload
```

**Terminal 4 - WebSocket Bridge**:
```bash
cd backend/websocket-bridge
python main.py
```

### Step 4: Verify Backend Health

```bash
# Check agent health endpoints
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8006/health

# Expected: {"status":"healthy","uptime_seconds":...}
```

### Step 5: Start Frontend

```bash
cd mystery-skils-app-ui

# Install dependencies (first time only)
npm install

# Start development server (port 4000)
npm run dev
```

Open browser: **http://localhost:4000**

---

## 🧪 Testing the System

### Test 1: Health Checks

```bash
# Triage Agent
curl http://localhost:8001/health
# Expected: {"status":"healthy","uptime_seconds":X}

# Concepts Agent
curl http://localhost:8002/health

# Progress Tracker
curl http://localhost:8006/health

# All /ready endpoints
curl http://localhost:8001/ready
curl http://localhost:8002/ready
curl http://localhost:8006/ready
```

### Test 2: Query Classification (Triage Agent)

```bash
curl -X POST http://localhost:8001/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "query_id": "test-001",
    "student_id": "student-123",
    "query_text": "What is recursion in Python?"
  }'
```

**Expected Response**:
```json
{
  "query_id": "test-001",
  "detected_intent": "CONCEPT_EXPLANATION",
  "confidence_score": 0.85,
  "routed_to_agent": "concepts-agent",
  "extracted_entities": {
    "topics": ["recursion"],
    "difficulty": "beginner"
  },
  "reasoning": "Student asking for concept explanation",
  "processing_time_ms": 1234
}
```

### Test 3: Concept Explanation (Concepts Agent)

```bash
curl -X POST http://localhost:8002/api/v1/explain \
  -H "Content-Type": application/json" \
  -d '{
    "query_id": "test-002",
    "student_id": "student-123",
    "concept": "recursion",
    "difficulty_level": "beginner",
    "include_examples": true
  }'
```

**Expected**: Detailed explanation with code examples

### Test 4: Mastery Tracking (Progress Tracker)

```bash
# Get student mastery
curl http://localhost:8006/api/v1/mastery/student-123

# Update mastery
curl -X POST http://localhost:8006/api/v1/mastery/student-123 \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "student-123",
    "topic": "recursion",
    "interaction_type": "success",
    "success": true
  }'
```

### Test 5: Frontend Integration

1. Open **http://localhost:4000** in browser
2. **Verify**:
   - ✅ WebSocket status shows "Connected" (green dot)
   - ✅ Student mastery loads (7 Python topics displayed)
   - ✅ Agent logs appear in real-time
   - ✅ Overall mastery percentage shows

3. **Trigger an event** (in backend terminal):
```bash
# Update student mastery (should appear in UI immediately)
curl -X POST http://localhost:8006/api/v1/mastery/demo-student-001 \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "demo-student-001",
    "topic": "functions",
    "interaction_type": "success",
    "success": true
  }'
```

4. **Check UI for**:
   - Mastery update appears in "Mastery Updates" section
   - Overall mastery percentage increases
   - Agent log shows "Progress Tracker" activity

---

## 🔍 Troubleshooting

### Backend Issues

**Agent won't start**:
```bash
# Check if port is already in use
netstat -ano | findstr :8001  # Windows
lsof -i :8001  # macOS/Linux

# Kill process if needed
taskkill /PID <pid> /F  # Windows
kill -9 <pid>  # macOS/Linux
```

**Import errors**:
```bash
# Make sure you're in venv
which python  # Should show venv/bin/python

# Reinstall dependencies
pip install -r backend/requirements.txt
```

**Kafka connection errors**:
```bash
# Restart Docker Compose
docker-compose down
docker-compose up -d

# Check logs
docker-compose logs kafka
```

### Frontend Issues

**npm install fails**:
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

**WebSocket won't connect**:
```bash
# Check WebSocket bridge is running
curl http://localhost:4001/health

# Check browser console for errors
# Open DevTools → Console
```

**Mastery data not loading**:
```bash
# Check Progress Tracker is running
curl http://localhost:8006/health

# Check API route
curl http://localhost:4000/api/mastery?studentId=demo-student-001
```

---

## 📊 Monitoring

### Agent Metrics (Prometheus)

```bash
# Triage Agent metrics
curl http://localhost:8001/metrics

# Concepts Agent metrics
curl http://localhost:8002/metrics

# Progress Tracker metrics
curl http://localhost:8006/metrics
```

### Kafka Topics

```bash
# List topics
docker exec -it kafka kafka-topics \
  --bootstrap-server localhost:9092 \
  --list

# Consume from topic (real-time)
docker exec -it kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic mastery-updates \
  --from-beginning
```

---

## 🛑 Shutdown

```bash
# Stop frontend
# Ctrl+C in mystery-skils-app-ui terminal

# Stop backend agents
# Ctrl+C in each agent terminal

# Stop Docker infrastructure
docker-compose down
```

---

## 🚢 Production Deployment (Kubernetes)

### Prerequisites
```bash
# Install Minikube
minikube start

# Install Dapr CLI
dapr init --kubernetes
```

### Deploy

```bash
# Apply Dapr components
kubectl apply -f infrastructure/dapr/components/

# Deploy agents
./infrastructure/scripts/deploy-local.sh

# Verify deployment
kubectl get pods
kubectl get services
```

---

## 📝 Next Steps

### Add Remaining Agents

After testing the core 3-agent system, add:

1. **Code Review Agent** (Port 8003)
2. **Debug Agent** (Port 8004)
3. **Exercise Generator** (Port 8005)

### Production Readiness

- [ ] Add authentication (BetterAuth recommended)
- [ ] Configure TLS/SSL certificates
- [ ] Set up monitoring (Prometheus + Grafana)
- [ ] Configure log aggregation (ELK stack)
- [ ] Implement rate limiting
- [ ] Set up CI/CD pipeline

---

## 🆘 Support

**Issues**: https://github.com/anthropics/claude-code/issues
**Documentation**: See `specs/002-learnflow-platform/`
**Architecture**: See `AGENTS.md`
