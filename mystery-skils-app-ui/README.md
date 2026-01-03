# Mystery Skills - 3D Learning Mastery Platform

A real-time visualization platform for student learning progress with AI agent monitoring.

## 🎨 What's Built

### ✅ Frontend (Complete)

**3D Mastery Sphere** (`components/ui/MasterySphere.tsx`)
- Rotating 3D sphere with 7 mastery rings (Python curriculum)
- Color progression: Red (0%) → Orange (33%) → Green (66%) → Blue (100%)
- Real-time updates as students progress
- Interactive 3D controls (zoom, rotate)

**Hacker Terminal** (`components/ui/HackerTerminal.tsx`)
- Real-time agent log viewer
- Color-coded by log level (INFO/WARN/ERROR/SUCCESS)
- Auto-scrolling terminal with scanline effects
- Connected to WebSocket for live Dapr/Kafka streams

**Teacher HUD** (`components/ui/TeacherHUD.tsx`)
- Student monitoring dashboard
- **Struggle Detection**: Pulses RED when student hits 5+ failed runs
- Shows current topic, failed run count, last activity
- Real-time alerts for struggling students

### 🔧 Tech Stack

- **Next.js 15** (App Router)
- **React 19** + TypeScript
- **Three.js** + @react-three/fiber (3D graphics)
- **Framer Motion** (animations)
- **Socket.io-client** (real-time WebSocket)
- **Tailwind CSS** (styling)

---

## 🚀 Quick Start

### 1. Run the UI (Port 4000)

```bash
cd mystery-skils-app-ui
npm run dev
```

Open: **http://localhost:4000**

You should see:
- **3D Sphere** in center with 7 rotating rings
- **Hacker Terminal** on right with simulated logs
- **Teacher HUD** on left with demo students

---

## 🔌 Integration Guide

### What's Working NOW (Demo Mode)

✅ UI fully functional with **simulated data**
✅ 3D Sphere rotates with color-coded rings
✅ Terminal shows mock agent logs
✅ Teacher HUD displays 3 demo students (1 struggling)

### What Needs Backend Connection

❌ Real student mastery levels (currently random 0-100)
❌ Real agent logs from LearnFlow agents
❌ Real struggle detection from student activity
❌ Authentication (no login yet)

---

## 📋 Next Steps - Backend Integration

### Step 1: Build LearnFlow Backend Agents

**You have the spec ready!** (`specs/002-learnflow-platform/spec.md`)

Run this to start implementation:

```bash
/sp.plan          # Create implementation plan
/sp.tasks         # Generate task breakdown
/sp.implement     # Build the 6 FastAPI agents
```

**6 Agents to Build:**
1. **Triage Agent** (port 8001) - Routes student queries
2. **Concepts Agent** (port 8002) - Explains programming concepts
3. **Code Review Agent** (port 8003) - Reviews student code
4. **Debug Agent** (port 8004) - Helps debug errors
5. **Exercise Generator** (port 8005) - Creates practice problems
6. **Progress Tracker** (port 8006) - Tracks student learning

### Step 2: Create Backend API for Mystery Skills

Create `mystery-skils-app-ui/app/api/` routes:

**`api/mastery/route.ts`** - Get student mastery levels
```typescript
export async function GET() {
  // Fetch from Progress Tracker agent (port 8006)
  const response = await fetch('http://localhost:8006/mastery/student123')
  const data = await response.json()
  return Response.json({ levels: data.pythonCurriculum })
}
```

**`api/socket/route.ts`** - WebSocket server for real-time logs
```typescript
// Connect to Dapr/Kafka pub/sub
// Forward agent logs to frontend via Socket.io
```

### Step 3: Wire Up Dapr/Kafka

**Backend: Publish Events**
```python
# In each FastAPI agent
import dapr.clients

dapr_client = dapr.clients.DaprClient()

# When agent processes query
dapr_client.publish_event(
    pubsub_name="kafka-pubsub",
    topic_name="agent-logs",
    data={"agent": "CONCEPTS", "level": "INFO", "message": "Processing query..."}
)

# When student struggles (5+ failures)
dapr_client.publish_event(
    pubsub_name="kafka-pubsub",
    topic_name="student-struggle",
    data={"studentId": "STU001", "failedRuns": 6, "topic": "Recursion"}
)
```

**Frontend: Subscribe via WebSocket**
Already set up in `lib/hooks/useAgentLogs.ts` - just point to your backend Socket.io server.

### Step 4: Authentication (BetterAuth Recommended)

**Why BetterAuth?**
- ✅ Modern, TypeScript-first
- ✅ Works seamlessly with Next.js 15
- ✅ Built-in session management
- ✅ Easy to integrate

**Install:**
```bash
npm install better-auth
```

**Setup:**
1. Create `lib/auth.ts` with BetterAuth config
2. Add login/signup pages
3. Protect dashboard routes
4. Add user context to mastery/logs APIs

---

## 🎯 Current Project Status

### ✅ COMPLETED

1. **agents-md-gen skill** (001) - Auto-generates AGENTS.md from FastAPI code
2. **LearnFlow spec** (002) - Complete specification for 6-agent system
3. **Mystery Skills UI** - 3D visualization platform (this repo)

### 🚧 IN PROGRESS

4. **LearnFlow Backend** - Need to implement 6 FastAPI agents
   - Status: Spec complete, ready for `/sp.plan`

### ⏳ TODO

5. **Backend Integration** - Connect Mystery Skills UI to LearnFlow
6. **Dapr/Kafka Setup** - Real-time pub/sub messaging
7. **Authentication** - BetterAuth integration
8. **Mastery Tracking** - Logic to update rings based on student progress
9. **Struggle Detection Backend** - Track failed runs, trigger alerts

---

## 🗂️ File Structure

```
mystery-skils-app-ui/
├── app/
│   ├── page.tsx              # Main dashboard
│   ├── layout.tsx            # Root layout
│   ├── globals.css           # Global styles + animations
│   └── api/                  # [TODO] Backend API routes
│       ├── mastery/route.ts  # Mastery levels endpoint
│       └── auth/[...].ts     # BetterAuth endpoints
├── components/ui/
│   ├── MasterySphere.tsx     # 3D Sphere with rings ✅
│   ├── HackerTerminal.tsx    # Real-time logs ✅
│   └── TeacherHUD.tsx        # Struggle detection ✅
├── lib/hooks/
│   ├── useMasteryState.ts    # Mastery data hook ✅
│   └── useAgentLogs.ts       # WebSocket logs hook ✅
└── package.json              # Dependencies ✅
```

---

## 🔗 How Frontend/Backend Match

| **Frontend Component** | **Backend Source** | **Status** |
|------------------------|-------------------|------------|
| 3D Sphere Rings | Progress Tracker Agent (port 8006) `/mastery` | ⏳ Need backend |
| Hacker Terminal | Dapr/Kafka `agent-logs` topic via WebSocket | ⏳ Need backend |
| Teacher HUD | Dapr/Kafka `student-struggle` topic | ⏳ Need backend |
| Mastery Progress | Progress Tracker tracks completed exercises | ⏳ Need backend |

---

## 🎬 Demo vs Production

**Current (Demo Mode):**
- Simulated data in `lib/hooks/useAgentLogs.ts:simulateInitialData()`
- Random mastery levels in `lib/hooks/useMasteryState.ts`
- 3 hardcoded demo students

**Production (After Backend Integration):**
- Real student data from Progress Tracker agent
- Live agent logs from all 6 LearnFlow agents
- Actual struggle detection based on student code runs
- User authentication with student profiles

---

## 🚨 Critical Next Action

**Run this command to start building the backend:**

```bash
/sp.plan   # For LearnFlow (002-learnflow-platform)
```

This will create the implementation plan for all 6 FastAPI agents. Then run `/sp.tasks` and `/sp.implement` to build them.

Once agents are running, you can connect them to Mystery Skills UI via the API routes mentioned above.

---

## 📞 Support

Built with **Claude Code** - Spec-Driven Development (SDD-RI) methodology

- Spec: `specs/002-learnflow-platform/spec.md`
- Constitution: `.specify/memory/constitution.md`
