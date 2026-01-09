<div align="center">

# MYSTERY SKILLS

### *The Future of AI-Powered Learning*

[![Live Demo](https://img.shields.io/badge/LIVE_DEMO-Click_Here-00ffcc?style=for-the-badge&logo=netlify)](https://mystery-skills.netlify.app)
[![Backend API](https://img.shields.io/badge/API-Online-39ff14?style=for-the-badge&logo=fastapi)](https://reusable-intelligence.onrender.com/health)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)](https://python.org)
[![Next.js](https://img.shields.io/badge/Next.js-15-black?style=for-the-badge&logo=next.js)](https://nextjs.org)

<img src="https://img.shields.io/badge/AI_Agents-6-ff3131?style=flat-square" />
<img src="https://img.shields.io/badge/Coding_Challenges-22+-ffaa00?style=flat-square" />
<img src="https://img.shields.io/badge/Real--Time-Notifications-00f0ff?style=flat-square" />

---

**An immersive cyberpunk-themed learning platform where AI meets education.**

*Teachers assign. Students learn. AI assists. Everyone wins.*

[Live Demo](https://mystery-skills.netlify.app) | [API Health](https://reusable-intelligence.onrender.com/health) | [Report Bug](https://github.com/AlishbaFatima12/reusable_intelligence/issues)

</div>

---

## What Makes Mystery Skills Special?

```
+------------------------------------------------------------------+
|                                                                  |
|   "Not just another learning platform.                           |
|    It's an AI-powered command center for mastering code."        |
|                                                                  |
+------------------------------------------------------------------+
```

| For Students | For Teachers |
|:------------:|:------------:|
| Practice with AI-generated quizzes | Monitor all students in real-time |
| Code directly in browser | Assign MCQs & coding challenges |
| Get instant AI code reviews | Send encouragement notes |
| Earn XP, badges & streaks | Track completion & scores |
| 22+ coding challenges | Auto-generate fresh questions |

---

## Live Demo

### Try It Now - No Installation Required!

| Platform | URL | Status |
|----------|-----|--------|
| **Frontend** | [mystery-skills.netlify.app](https://mystery-skills.netlify.app) | ![Netlify](https://img.shields.io/badge/Live-00ffcc) |
| **Backend API** | [reusable-intelligence.onrender.com](https://reusable-intelligence.onrender.com/health) | ![Render](https://img.shields.io/badge/Live-39ff14) |

### Quick Test:
1. Visit the [Live Demo](https://mystery-skills.netlify.app)
2. **Register as Teacher** - Create assignments
3. **Register as Student** (in incognito) - Complete assignments
4. Watch real-time notifications flow between dashboards!

---

## Core Features

### Student Dashboard

| Feature | Description |
|---------|-------------|
| **Practice Topics** | 8 categories: Python, Data Structures, Algorithms, OOP, and more |
| **Code Lab** | Write & run Python code directly in browser - no setup needed |
| **AI Code Review** | Submit code and get instant AI feedback |
| **22+ Challenges** | From "Print Hello World" to "Fibonacci Sequence" |
| **Custom Problems** | Type any topic - AI generates a challenge instantly |
| **Real-Time Alerts** | Instant popups when teacher assigns work |
| **Gamification** | XP points, day streaks, achievements, confetti celebrations |

### Teacher Dashboard

| Feature | Description |
|---------|-------------|
| **Student Overview** | See all students, their progress, and scores |
| **MCQ Generator** | AI creates fresh questions every time |
| **Assign Tasks** | Send MCQs or coding challenges with one click |
| **Send Notes** | Encourage high performers, remind slackers |
| **Track Progress** | View who completed what and when |
| **Struggle Detection** | AI identifies students who need help |

---

## The Tech Behind The Magic

### 6 AI Agents Working Together

```
                    +------------------+
                    |   TRIAGE AGENT   |  <-- Routes your question
                    |     (Port 8001)  |
                    +--------+---------+
                             |
         +-------------------+-------------------+
         |         |         |         |         |
    +----+----+ +--+---+ +---+---+ +---+--+ +----+----+
    |CONCEPTS | |DEBUG | |REVIEW | |EXER- | |PROGRESS |
    | AGENT   | |AGENT | | AGENT | |CISE  | | TRACKER |
    | (8002)  | |(8004)| | (8003)| |(8005)| |  (8006) |
    +---------+ +------+ +-------+ +------+ +---------+
```

| Agent | What It Does |
|-------|-------------|
| **Triage** | Understands your question & routes to the right agent |
| **Concepts** | Explains programming topics + generates MCQs |
| **Code Review** | Analyzes your code and suggests improvements |
| **Debug** | Helps find and fix errors in your code |
| **Exercise** | Generates fresh coding challenges |
| **Progress** | Tracks mastery, XP, and learning patterns |

### Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Next.js 15, TypeScript, Tailwind CSS, Three.js |
| **Backend** | FastAPI, Python 3.11+, Uvicorn |
| **Database** | PostgreSQL (Neon), Prisma ORM |
| **AI** | OpenAI GPT-4o-mini |
| **Deployment** | Netlify (Frontend), Render (Backend) |

---

## Coding Challenges

### 22+ Challenges Across 4 Difficulty Levels

<details>
<summary><b>Beginner (Click to expand)</b></summary>

- Print Hello World
- Add Two Numbers
- Find String Length
- Access List Item
- Loop Through List
- Check Number (if/else)

</details>

<details>
<summary><b>Easy</b></summary>

- Reverse a String
- Sum of List
- Find Maximum
- Sort a List

</details>

<details>
<summary><b>Medium</b></summary>

- Count Vowels
- Filter Even Numbers
- Calculate Factorial
- Check Palindrome
- FizzBuzz
- List Comprehension

</details>

<details>
<summary><b>Hard</b></summary>

- Word Frequency Counter
- Check Prime Number
- Fibonacci Sequence
- Create a Class

</details>

---

## Quick Start (Local Development)

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL (or free [Neon](https://neon.tech) account)

### 1. Clone & Install

```bash
git clone https://github.com/AlishbaFatima12/reusable_intelligence.git
cd reusable_intelligence

# Frontend
cd mystery-skils-app-ui
npm install
```

### 2. Environment Setup

Create `.env` in `mystery-skils-app-ui/`:
```env
DATABASE_URL="postgresql://user:pass@host:5432/db"
BETTER_AUTH_SECRET="your-secret-key"
```

Create `.env` in root:
```env
OPENAI_API_KEY="sk-your-key"
```

### 3. Database Setup

```bash
cd mystery-skils-app-ui
npx prisma db push
```

### 4. Run Everything

```bash
# Terminal 1: Frontend
cd mystery-skils-app-ui
npm run dev

# Terminal 2: Backend (all agents)
cd backend
pip install -r requirements-deploy.txt
python server.py
```

### 5. Open App

Visit: **http://localhost:4000**

---

## API Reference

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login user |
| GET | `/api/auth/students` | Get all students |

### Assignments
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/assignments` | Create assignment |
| GET | `/api/assignments/student/:id` | Get student's assignments |
| PUT | `/api/assignments/:id/complete` | Mark as complete |

### AI Agents (Production)
| Endpoint | Description |
|----------|-------------|
| `POST /api/v1/triage/analyze` | Analyze & route query |
| `POST /api/v1/concepts/explain` | Explain a concept |
| `POST /api/v1/concepts/generate-mcqs` | Generate MCQ questions |
| `POST /api/v1/code-review/review` | Review code |
| `POST /api/v1/debug/diagnose` | Debug code errors |
| `POST /api/v1/exercise/generate` | Generate exercises |
| `GET /api/v1/progress/mastery/:id` | Get student mastery |

---

## Screenshots

<div align="center">

### Student Dashboard
*Practice topics, complete challenges, earn XP*

### Teacher Dashboard
*Monitor students, assign tasks, track progress*

### Code Lab
*Write, run, and review Python code in browser*

</div>

---

## Contributing

```bash
# Fork the repo, then:
git checkout -b feature/your-feature
git commit -m "Add your feature"
git push origin feature/your-feature
# Open a Pull Request
```

---

## Team

| Role | Name |
|------|------|
| **Developer** | [@AlishbaFatima12](https://github.com/AlishbaFatima12) |
| **AI Assistant** | Claude (Anthropic) |

---

## License

MIT License - Free to use, modify, and distribute.

---

<div align="center">

### Built for the Future of Learning

[![Star this repo](https://img.shields.io/github/stars/AlishbaFatima12/reusable_intelligence?style=social)](https://github.com/AlishbaFatima12/reusable_intelligence)

**[Try Live Demo](https://mystery-skills.netlify.app)** | **[View API](https://reusable-intelligence.onrender.com/health)** | **[Report Issues](https://github.com/AlishbaFatima12/reusable_intelligence/issues)**

---

*"Where AI meets education, and learning becomes an adventure."*

</div>
