# LearnFlow - AI-Powered Learning Platform

**Transform the way you learn programming with AI-powered personalized education**

---

## What is LearnFlow?

LearnFlow is a modern **AI-powered learning platform** designed for programming education. It provides a unique experience where **teachers can assign tasks** and **students can practice coding** with real-time AI assistance.

### Live Demo
> **URL**: _Coming Soon_

---

## Key Features

### For Students

| Feature | Description |
|---------|-------------|
| **Practice Topics** | Interactive MCQ quizzes on Python, Data Structures, Algorithms, and more |
| **Code Lab** | Write and run Python code directly in the browser |
| **22+ Coding Challenges** | From beginner to advanced - Print Hello World to Fibonacci |
| **Custom Problem Generator** | Type any topic and generate a coding challenge instantly |
| **AI Code Review** | Get instant feedback on your code from AI |
| **Real-time Notifications** | Instant popups when teachers assign tasks |
| **Progress Tracking** | XP points, achievements, and learning streaks |
| **Gamification** | Confetti celebrations, badges, and level progression |

### For Teachers

| Feature | Description |
|---------|-------------|
| **Student Dashboard** | View all students and their progress at a glance |
| **Assign MCQ Tests** | Create and assign practice tests on any topic |
| **Assign Coding Challenges** | Send coding tasks to students with one click |
| **Send Notes & Reminders** | Encourage students or send deadline reminders |
| **View Completions** | Track which students completed assignments |
| **Auto-Generate Questions** | AI generates fresh questions every time |

---

## Screenshot Preview

```
+------------------------------------------+
|  LEARNFLOW                    [Teacher]  |
+------------------------------------------+
|                                          |
|  STUDENTS          CENTER PANEL          |
|  +--------+   +---------------------+    |
|  | Alishba|   |  PRACTICE TOPICS    |    |
|  | Ali    |   |  [Python] [Data]    |    |
|  | Sara   |   |  [Algo]  [OOP]      |    |
|  +--------+   +---------------------+    |
|                                          |
|  TEACHER ACTIONS                         |
|  +------------------+                    |
|  | ASSIGN MCQ TEST  |                    |
|  | ASSIGN CODE TASK |                    |
|  +------------------+                    |
+------------------------------------------+
```

---

## Technology Stack

### Frontend
- **Next.js 15** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Modern styling with glassmorphism
- **In-browser Python** - Run Python code without backend

### Backend (6 AI Agents)
| Agent | Port | Purpose |
|-------|------|---------|
| Triage Agent | 8001 | Route queries to correct agent |
| Concepts Agent | 8002 | Explain programming concepts + Generate MCQs |
| Code Review Agent | 8003 | Review student code with AI feedback |
| Debug Agent | 8004 | Help debug code errors |
| Exercise Generator | 8005 | Generate coding exercises |
| Progress Tracker | 8006 | Track student mastery and progress |

### Database
- **PostgreSQL** (via Neon) - Store users, assignments, notifications
- **Prisma ORM** - Type-safe database access

### AI
- **Claude API** (Anthropic) - Powers all AI features

---

## Quick Start (Local Development)

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL database (or use Neon free tier)

### 1. Clone Repository
```bash
git clone https://github.com/AlishbaFatima12/reusable_intelligence.git
cd reusable_intelligence
```

### 2. Setup Frontend
```bash
cd mystery-skils-app-ui
npm install
cp .env.example .env
# Edit .env with your DATABASE_URL and ANTHROPIC_API_KEY
npx prisma db push
npm run dev
```

### 3. Setup Backend Agents
```bash
cd ..
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r backend/requirements.txt
```

### 4. Start All Agents
```bash
# Windows
start-agents.bat

# Or manually start each agent:
python -m uvicorn backend.agents.triage.main:app --port 8001
python -m uvicorn backend.agents.concepts.main:app --port 8002
# ... etc
```

### 5. Access the App
Open http://localhost:4000/mystery-skills-flash.html

---

## User Guide

### Student Flow
1. **Register** as a student with email/password
2. Click **PRACTICE TOPICS** to take MCQ quizzes
3. Click **CODE LAB** to practice coding challenges
4. Use **RUN CODE** to execute your Python code
5. Use **REVIEW** to get AI feedback on your code
6. Check **notifications** for teacher assignments
7. Complete assignments to earn **XP and achievements**

### Teacher Flow
1. **Register** as a teacher with email/password
2. View all registered **students** in left panel
3. Click a student to see their **progress and assignments**
4. **Generate MCQ Test**: Select topic → Generate → Assign to students
5. **Assign Coding Task**: Select students → Select challenge → Assign
6. Send **appreciation notes** to high performers
7. Send **reminders** for pending assignments

---

## Coding Challenges Available

### Beginner
- Print Hello World
- Add Two Numbers
- Find String Length
- Access List Item
- Loop Through List
- Check Number (if/else)

### Easy
- Reverse a String
- Sum of List
- Find Maximum
- Sort a List

### Medium
- Count Vowels
- Filter Even Numbers
- Calculate Factorial
- Check Palindrome
- FizzBuzz
- List Comprehension

### Hard
- Word Frequency Counter
- Check Prime Number
- Fibonacci Sequence
- Create a Class

---

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/students` - Get all students (teacher only)

### Assignments
- `POST /api/assignments` - Create assignment
- `GET /api/assignments/student/:id` - Get student assignments
- `PUT /api/assignments/:id/complete` - Mark complete

### Notifications
- `GET /api/notifications/:userId` - Get user notifications
- `POST /api/notifications` - Create notification
- `PUT /api/notifications/:id/mark-read` - Mark as read

### AI Agents
- `POST :8002/api/v1/generate-mcqs` - Generate MCQ questions
- `POST :8002/api/v1/explain` - Explain a concept
- `POST :8003/api/v1/review` - Review code
- `GET :8006/api/v1/mastery/:studentId` - Get student mastery

---

## Environment Variables

```env
# Database
DATABASE_URL="postgresql://user:pass@host:5432/db"

# AI
ANTHROPIC_API_KEY="sk-ant-..."

# Optional
CLAUDE_MODEL="claude-sonnet-3-5-20241022"
```

---

## Deployment

### Frontend (Vercel - Recommended)
1. Push to GitHub
2. Connect repo to Vercel
3. Set environment variables
4. Deploy automatically

### Backend (Railway/Render)
1. Deploy each agent as separate service
2. Set ANTHROPIC_API_KEY
3. Configure ports 8001-8006

---

## Project Structure

```
reusable_intelligence/
├── mystery-skils-app-ui/     # Next.js frontend
│   ├── app/                  # App router pages
│   │   ├── api/             # API routes
│   │   ├── auth/            # Auth pages
│   │   ├── student/         # Student dashboard
│   │   └── teacher/         # Teacher dashboard
│   ├── public/
│   │   └── mystery-skills-flash.html  # Main UI
│   └── prisma/
│       └── schema.prisma    # Database schema
├── backend/                  # Python microservices
│   └── agents/
│       ├── triage/          # Query routing
│       ├── concepts/        # MCQ generation
│       ├── code_review/     # Code review
│       ├── debug/           # Debugging help
│       ├── exercise/        # Exercise generation
│       └── progress/        # Progress tracking
└── README.md
```

---

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## License

MIT License - feel free to use for your own learning projects!

---

## Credits

- **Team**: AlishbaFatima12
- **Hackathon**: Reusable Intelligence & Cloud-Native Mastery
- **AI**: Powered by Claude (Anthropic)

---

## Support

Having issues?
- Open a GitHub issue
- Check the browser console for errors
- Ensure all agents are running (ports 8001-8006)

---

**Built with AI, for AI-powered learning**
