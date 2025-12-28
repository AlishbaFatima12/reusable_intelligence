# Hackathon III: Strategic Roadmap
## Reusable Intelligence and Cloud-Native Mastery

**Last Updated:** 2025-12-27
**Project:** LearnFlow AI-Powered Learning Platform
**Repositories:** `skills-library` + `learnflow-app`

---

## 🎯 Mission-Critical Success Factors

### 1. Token Efficiency (Target: 80-98% Reduction)
**Problem from Previous Hackathons:**
- Direct MCP integration consumed 50k+ tokens before conversation started
- Intermediate results bloated context window
- Skills loaded entire tool definitions into memory

**Solution for Hackathon III:**
```
BEFORE (Hackathon 2):  Direct MCP → 50k tokens at startup
AFTER (Hackathon 3):   Skills + Scripts → ~100 tokens per skill
```

**Implementation Pattern:**
```
.claude/skills/<skill-name>/
├── SKILL.md          (~100 tokens - loaded on demand)
├── REFERENCE.md      (0 tokens - loaded only if needed)
└── scripts/
    ├── deploy.sh     (0 tokens - executed, never loaded)
    └── verify.py     (0 tokens - returns minimal output)
```

### 2. Avoiding Previous Mistakes

| Previous Issue | Root Cause | Hackathon III Solution |
|---------------|------------|------------------------|
| Repeated bugs | Manual code writing | Let agents write code via skills |
| High quota usage | MCP bloat | MCP Code Execution pattern |
| Integration failures | Tight coupling | Modular skills with validation |
| Deployment errors | Manual steps | Automated scripts in skills |
| Cross-agent incompatibility | Claude-specific patterns | AAIF-compliant skills |

### 3. Autonomous Deployment Goal
**Gold Standard:** Single prompt → Running K8s deployment with zero manual intervention

```bash
# User types ONE command:
"Deploy Kafka to Kubernetes"

# Agent autonomously:
1. Loads kafka-k8s-setup/SKILL.md (~100 tokens)
2. Executes scripts/deploy.sh (0 tokens loaded)
3. Runs scripts/verify.py (0 tokens loaded)
4. Returns: "✓ All 3 pods running" (~10 tokens)
# Total context cost: ~110 tokens
```

---

## 📋 Phase-by-Phase Execution Plan

### Phase 1: Environment Setup (Day 1)
**Duration:** 2-4 hours
**Priority:** CRITICAL - Everything depends on this

#### Actions:
```bash
# 1.1 Install Prerequisites
# Windows: Use WSL for all development
wsl --install Ubuntu-22.04

# Docker
sudo apt-get update
sudo apt-get install docker.io docker-compose
sudo usermod -aG docker $USER

# Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Claude Code
curl -fsSL https://claude.ai/install.sh | bash
claude auth login

# Goose
curl -fsSL https://github.com/block/goose/releases/download/stable/download_cli.sh | bash
```

#### Validation Script:
```bash
#!/bin/bash
echo "🔍 Verifying Hackathon III Environment..."

# Check Docker
docker --version || echo "❌ Docker missing"

# Check Minikube
minikube version || echo "❌ Minikube missing"

# Start Minikube
minikube start --cpus=4 --memory=8192 --driver=docker

# Check Kubernetes
kubectl cluster-info || echo "❌ Kubernetes not accessible"

# Check Helm
helm version || echo "❌ Helm missing"

# Check Claude Code
claude --version || echo "❌ Claude Code missing"

# Check Goose
goose --version || echo "❌ Goose missing"

echo "✅ Environment ready for Hackathon III"
```

#### Success Criteria:
- [ ] Minikube cluster running
- [ ] kubectl returns cluster info
- [ ] Both Claude Code and Goose authenticated
- [ ] Docker containers can be built

---

### Phase 2: Repository Structure (Day 1)
**Duration:** 1 hour
**Priority:** HIGH

#### Create Skills Library Repository:
```bash
mkdir skills-library && cd skills-library
git init

# Create standard structure
mkdir -p .claude/skills
mkdir -p docs
mkdir -p examples

# Create README
cat > README.md << 'EOF'
# Skills Library - Hackathon III
## Reusable Intelligence for Cloud-Native Development

This repository contains production-ready skills that work with:
- ✅ Claude Code (Anthropic)
- ✅ Goose (AAIF Standard)
- ✅ OpenAI Codex

## Skills Included

| Skill | Purpose | Token Cost |
|-------|---------|------------|
| agents-md-gen | Generate AGENTS.md files | ~100 |
| kafka-k8s-setup | Deploy Kafka on K8s | ~110 |
| postgres-k8s-setup | Deploy PostgreSQL on K8s | ~105 |
| fastapi-dapr-agent | Create FastAPI+Dapr services | ~120 |
| mcp-code-execution | MCP with code execution | ~95 |
| nextjs-k8s-deploy | Deploy Next.js apps | ~115 |
| docusaurus-deploy | Deploy documentation | ~100 |

**Total token cost:** ~745 tokens for 7 complete deployment skills
**vs Direct MCP:** 50,000+ tokens for equivalent functionality
**Savings:** 98.5%

## Usage

### With Claude Code:
```bash
cd your-project
cp -r ../skills-library/.claude .
claude "Deploy Kafka to Kubernetes"
```

### With Goose:
```bash
cd your-project
ln -s ../skills-library/.claude .
goose run "Deploy PostgreSQL with migrations"
```
EOF

# Initialize git
git add .
git commit -m "Initialize skills-library for Hackathon III"
```

#### Create LearnFlow Application Repository:
```bash
cd ..
mkdir learnflow-app && cd learnflow-app
git init

# Link to skills library
ln -s ../skills-library/.claude .claude

# Create project structure
mkdir -p {backend,frontend,infrastructure,docs}

# Create AGENTS.md (will be generated by agents-md-gen skill later)
touch AGENTS.md

git add .
git commit -m "Initialize LearnFlow application for Hackathon III"
```

---

### Phase 3: Foundation Skills (Day 1-2)
**Duration:** 4-6 hours
**Priority:** CRITICAL - All other skills depend on these

#### Skill 3.1: agents-md-gen
**Purpose:** Teach agents how to understand and work with your codebase

```bash
cd skills-library
mkdir -p .claude/skills/agents-md-gen/scripts
```

**File: `.claude/skills/agents-md-gen/SKILL.md`**
```markdown
---
name: agents-md-gen
description: Generate comprehensive AGENTS.md files for repositories
version: 1.0.0
---

# AGENTS.md Generator

## When to Use
- New repository needs agent-friendly documentation
- Existing project requires AGENTS.md
- Team adopting agentic development workflow

## What It Does
Creates a comprehensive AGENTS.md file that describes:
- Repository structure and organization
- Coding conventions and standards
- Build and deployment processes
- Testing strategies
- Common tasks and workflows

## Instructions

1. **Analyze repository structure:**
   ```bash
   python scripts/analyze_repo.py .
   ```

2. **Generate AGENTS.md:**
   ```bash
   python scripts/generate_agents_md.py . > AGENTS.md
   ```

3. **Validate output:**
   ```bash
   python scripts/validate_agents_md.py AGENTS.md
   ```

## Validation Checklist
- [ ] AGENTS.md exists in repository root
- [ ] All major directories documented
- [ ] Tech stack clearly listed
- [ ] Common commands included
- [ ] File passes validation script

## Expected Output
```
✓ Repository analyzed: 42 files, 8 directories
✓ AGENTS.md generated: 156 lines
✓ Validation passed: All sections present
```
```

**File: `.claude/skills/agents-md-gen/scripts/analyze_repo.py`**
```python
#!/usr/bin/env python3
"""Analyze repository structure for AGENTS.md generation."""
import os
import json
import sys
from pathlib import Path
from collections import defaultdict

def analyze_repository(repo_path):
    """Analyze repository structure and return metadata."""
    repo_path = Path(repo_path)

    structure = {
        "root": str(repo_path),
        "directories": [],
        "files_by_extension": defaultdict(list),
        "tech_stack": set(),
        "total_files": 0,
        "total_dirs": 0
    }

    # Walk directory tree
    for root, dirs, files in os.walk(repo_path):
        # Skip hidden and common ignore directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv']]

        rel_root = os.path.relpath(root, repo_path)
        if rel_root != '.':
            structure["directories"].append(rel_root)
            structure["total_dirs"] += 1

        for file in files:
            if file.startswith('.'):
                continue

            structure["total_files"] += 1
            ext = Path(file).suffix
            if ext:
                structure["files_by_extension"][ext].append(os.path.join(rel_root, file))

            # Detect tech stack
            if file == 'package.json':
                structure["tech_stack"].add("Node.js")
            elif file == 'requirements.txt' or file == 'pyproject.toml':
                structure["tech_stack"].add("Python")
            elif file == 'Dockerfile':
                structure["tech_stack"].add("Docker")
            elif file == 'docker-compose.yml':
                structure["tech_stack"].add("Docker Compose")
            elif ext == '.go':
                structure["tech_stack"].add("Go")
            elif ext == '.rs':
                structure["tech_stack"].add("Rust")

    structure["tech_stack"] = sorted(list(structure["tech_stack"]))

    # Output minimal summary
    print(f"✓ Analyzed: {structure['total_files']} files, {structure['total_dirs']} directories")
    print(f"✓ Tech stack detected: {', '.join(structure['tech_stack']) if structure['tech_stack'] else 'Unknown'}")

    # Save full analysis for next script
    with open('/tmp/repo_analysis.json', 'w') as f:
        json.dump(structure, f, indent=2, default=str)

    return structure

if __name__ == "__main__":
    repo_path = sys.argv[1] if len(sys.argv) > 1 else "."
    analyze_repository(repo_path)
```

**File: `.claude/skills/agents-md-gen/scripts/generate_agents_md.py`**
```python
#!/usr/bin/env python3
"""Generate AGENTS.md from repository analysis."""
import json
import sys
from pathlib import Path

def load_analysis():
    """Load repository analysis from temp file."""
    with open('/tmp/repo_analysis.json', 'r') as f:
        return json.load(f)

def generate_agents_md(analysis):
    """Generate AGENTS.md content."""
    tech_stack = analysis.get('tech_stack', [])

    md = f"""# AGENTS.md
## Repository Guide for AI Coding Agents

**Last Updated:** Auto-generated
**Repository:** {Path(analysis['root']).name}
**Tech Stack:** {', '.join(tech_stack) if tech_stack else 'Mixed'}

---

## 📁 Repository Structure

```
{Path(analysis['root']).name}/
"""

    # Add directory structure
    for dir_path in sorted(analysis['directories'][:10]):  # First 10 dirs
        md += f"├── {dir_path}/\n"

    md += """```

## 🛠️ Technology Stack

"""

    # Add tech stack details
    for tech in tech_stack:
        md += f"- **{tech}**\n"

    md += """
## 🚀 Common Commands

### Development
```bash
# Install dependencies
npm install  # or pip install -r requirements.txt

# Run development server
npm run dev  # or python main.py

# Run tests
npm test  # or pytest
```

### Deployment
```bash
# Build for production
npm run build  # or docker build -t app .

# Deploy
kubectl apply -f k8s/  # or helm install
```

## 📝 Coding Conventions

- **Language Style:** Follow language-specific best practices
- **File Naming:** Use kebab-case for files, PascalCase for classes
- **Documentation:** All public functions must have docstrings
- **Testing:** Minimum 80% code coverage required

## 🤖 AI Agent Instructions

When working with this repository:

1. **Always read this file first** to understand project structure
2. **Check existing patterns** before creating new files
3. **Run tests** after any code changes
4. **Update documentation** when adding features
5. **Follow commit conventions:** `type: description` (e.g., `feat: add user auth`)

## 📦 Key Files

"""

    # List important files
    important_extensions = {'.md', '.json', '.yml', '.yaml', '.toml'}
    for ext in important_extensions:
        if ext in analysis['files_by_extension']:
            for file in analysis['files_by_extension'][ext][:5]:
                md += f"- `{file}`\n"

    md += """
## 🔧 Troubleshooting

### Common Issues
- **Build fails:** Check dependency versions in package.json/requirements.txt
- **Tests fail:** Ensure test database is running
- **Deployment fails:** Verify Kubernetes cluster is accessible

---

**Note for AI Agents:** This file is auto-generated. When in doubt, analyze actual code files for ground truth.
"""

    return md

if __name__ == "__main__":
    analysis = load_analysis()
    md_content = generate_agents_md(analysis)
    print(md_content)
    print(f"\n✓ Generated AGENTS.md: {len(md_content.splitlines())} lines", file=sys.stderr)
```

**File: `.claude/skills/agents-md-gen/scripts/validate_agents_md.py`**
```python
#!/usr/bin/env python3
"""Validate AGENTS.md format and content."""
import sys

def validate_agents_md(file_path):
    """Validate AGENTS.md file."""
    required_sections = [
        "# AGENTS.md",
        "## Repository Structure",
        "## Technology Stack",
        "## Common Commands",
        "## AI Agent Instructions"
    ]

    try:
        with open(file_path, 'r') as f:
            content = f.read()

        missing = []
        for section in required_sections:
            if section not in content:
                missing.append(section)

        if missing:
            print(f"✗ Validation failed: Missing sections:")
            for section in missing:
                print(f"  - {section}")
            return False

        print(f"✓ Validation passed: All required sections present")
        return True

    except FileNotFoundError:
        print(f"✗ File not found: {file_path}")
        return False

if __name__ == "__main__":
    file_path = sys.argv[1] if len(sys.argv) > 1 else "AGENTS.md"
    success = validate_agents_md(file_path)
    sys.exit(0 if success else 1)
```

#### Test the Skill:
```bash
# With Claude Code
cd ../learnflow-app
claude "Generate AGENTS.md for this repository using agents-md-gen skill"

# With Goose (ensure .claude symlink exists)
goose run "Create AGENTS.md using the agents-md-gen skill"

# Verify output
cat AGENTS.md
```

**Success Criteria:**
- [ ] AGENTS.md generated in < 30 seconds
- [ ] File includes all required sections
- [ ] Works identically on Claude Code and Goose
- [ ] Total token cost < 150 tokens

---

### Phase 4: Infrastructure Skills (Day 2-3)
**Duration:** 6-8 hours
**Priority:** HIGH - Required for LearnFlow backend

#### Skill 4.1: kafka-k8s-setup

```bash
cd skills-library
mkdir -p .claude/skills/kafka-k8s-setup/scripts
```

**File: `.claude/skills/kafka-k8s-setup/SKILL.md`**
```markdown
---
name: kafka-k8s-setup
description: Deploy Apache Kafka on Kubernetes with verification
version: 1.0.0
---

# Kafka Kubernetes Setup

## When to Use
- Deploying event-driven microservices
- Need message queue for async communication
- Building LearnFlow backend infrastructure

## What It Does
- Deploys Kafka + Zookeeper to Kubernetes
- Creates namespace and configures resources
- Verifies all pods are running
- Creates test topic to confirm functionality

## Instructions

1. **Deploy Kafka:**
   ```bash
   bash scripts/deploy.sh
   ```

2. **Verify deployment:**
   ```bash
   python scripts/verify.py
   ```

3. **Create test topic (optional):**
   ```bash
   bash scripts/create_test_topic.sh
   ```

## Configuration
- **Namespace:** `kafka`
- **Replicas:** 1 (development), 3 (production)
- **Zookeeper Replicas:** 1 (development), 3 (production)

See [REFERENCE.md](./REFERENCE.md) for advanced configuration.

## Validation
- [ ] Kafka pods in Running state
- [ ] Zookeeper pods in Running state
- [ ] Can create and list topics
- [ ] Can produce and consume messages

## Expected Output
```
✓ Kafka deployed to namespace 'kafka'
✓ All 3 pods running
✓ Test topic created: hackathon-test
```
```

**File: `.claude/skills/kafka-k8s-setup/scripts/deploy.sh`**
```bash
#!/bin/bash
set -e

echo "🚀 Deploying Kafka to Kubernetes..."

# Add Bitnami Helm repo
helm repo add bitnami https://charts.bitnami.com/bitnami 2>/dev/null || true
helm repo update

# Create namespace
kubectl create namespace kafka --dry-run=client -o yaml | kubectl apply -f -

# Install Kafka
helm install kafka bitnami/kafka \
  --namespace kafka \
  --set replicaCount=1 \
  --set zookeeper.replicaCount=1 \
  --set persistence.enabled=false \
  --set zookeeper.persistence.enabled=false \
  --wait \
  --timeout 5m

echo "✓ Kafka deployed to namespace 'kafka'"
```

**File: `.claude/skills/kafka-k8s-setup/scripts/verify.py`**
```python
#!/usr/bin/env python3
"""Verify Kafka deployment on Kubernetes."""
import subprocess
import json
import sys
import time

def run_kubectl(args):
    """Run kubectl command and return output."""
    result = subprocess.run(
        ["kubectl"] + args,
        capture_output=True,
        text=True
    )
    return result.stdout, result.returncode

def verify_kafka():
    """Verify Kafka is running."""
    # Check pods
    stdout, code = run_kubectl(["get", "pods", "-n", "kafka", "-o", "json"])

    if code != 0:
        print("✗ Failed to get pods")
        return False

    pods = json.loads(stdout).get("items", [])

    if not pods:
        print("✗ No pods found in kafka namespace")
        return False

    running = sum(1 for p in pods if p["status"]["phase"] == "Running")
    total = len(pods)

    if running == total:
        print(f"✓ All {total} pods running")
        return True
    else:
        print(f"✗ Only {running}/{total} pods running")
        # List pod status
        for pod in pods:
            name = pod["metadata"]["name"]
            phase = pod["status"]["phase"]
            print(f"  - {name}: {phase}")
        return False

if __name__ == "__main__":
    max_retries = 3
    for attempt in range(max_retries):
        if verify_kafka():
            sys.exit(0)
        if attempt < max_retries - 1:
            print(f"Retrying in 10 seconds... ({attempt + 1}/{max_retries})")
            time.sleep(10)

    sys.exit(1)
```

**File: `.claude/skills/kafka-k8s-setup/REFERENCE.md`**
```markdown
# Kafka Kubernetes Setup - Reference Documentation

## Advanced Configuration

### Production Settings
```bash
helm install kafka bitnami/kafka \
  --namespace kafka \
  --set replicaCount=3 \
  --set zookeeper.replicaCount=3 \
  --set persistence.enabled=true \
  --set persistence.size=100Gi \
  --set resources.requests.memory=4Gi \
  --set resources.requests.cpu=2
```

### Custom Values
Create `kafka-values.yaml`:
```yaml
replicaCount: 3
heapOpts: "-Xmx4g -Xms4g"
persistence:
  enabled: true
  size: 100Gi
zookeeper:
  replicaCount: 3
  persistence:
    enabled: true
```

Deploy:
```bash
helm install kafka bitnami/kafka -f kafka-values.yaml
```

## Accessing Kafka

### From Inside Cluster
```
kafka.kafka.svc.cluster.local:9092
```

### From Outside Cluster (NodePort)
```bash
kubectl port-forward svc/kafka -n kafka 9092:9092
```

## Common Operations

### Create Topic
```bash
kubectl exec -it kafka-0 -n kafka -- kafka-topics.sh \
  --create \
  --topic my-topic \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 1
```

### List Topics
```bash
kubectl exec -it kafka-0 -n kafka -- kafka-topics.sh \
  --list \
  --bootstrap-server localhost:9092
```

### Produce Messages
```bash
kubectl exec -it kafka-0 -n kafka -- kafka-console-producer.sh \
  --topic my-topic \
  --bootstrap-server localhost:9092
```

### Consume Messages
```bash
kubectl exec -it kafka-0 -n kafka -- kafka-console-consumer.sh \
  --topic my-topic \
  --from-beginning \
  --bootstrap-server localhost:9092
```

## Troubleshooting

### Pods Not Starting
```bash
# Check events
kubectl get events -n kafka --sort-by='.lastTimestamp'

# Check pod logs
kubectl logs -n kafka kafka-0

# Check pod description
kubectl describe pod -n kafka kafka-0
```

### Connection Issues
```bash
# Test connectivity
kubectl exec -it kafka-0 -n kafka -- nc -zv localhost 9092
```

## Monitoring

### Check Broker Status
```bash
kubectl exec -it kafka-0 -n kafka -- kafka-broker-api-versions.sh \
  --bootstrap-server localhost:9092
```

### Check Consumer Groups
```bash
kubectl exec -it kafka-0 -n kafka -- kafka-consumer-groups.sh \
  --list \
  --bootstrap-server localhost:9092
```
```

---

#### Skill 4.2: postgres-k8s-setup

**File: `.claude/skills/postgres-k8s-setup/SKILL.md`**
```markdown
---
name: postgres-k8s-setup
description: Deploy PostgreSQL on Kubernetes with schema migrations
version: 1.0.0
---

# PostgreSQL Kubernetes Setup

## When to Use
- Need relational database for LearnFlow
- Storing user data, progress, quiz results
- Microservices require persistent storage

## What It Does
- Deploys PostgreSQL to Kubernetes
- Creates database and user
- Runs schema migrations
- Verifies connectivity

## Instructions

1. **Deploy PostgreSQL:**
   ```bash
   bash scripts/deploy.sh
   ```

2. **Run migrations:**
   ```bash
   python scripts/migrate.py
   ```

3. **Verify setup:**
   ```bash
   python scripts/verify.py
   ```

## Configuration
- **Namespace:** `database`
- **Database:** `learnflow`
- **User:** `learnflow_user`
- **Password:** Auto-generated (stored in Secret)

## Validation
- [ ] PostgreSQL pod running
- [ ] Database created
- [ ] Schema migrations applied
- [ ] Can connect and query

## Expected Output
```
✓ PostgreSQL deployed to namespace 'database'
✓ Database 'learnflow' created
✓ 5 migrations applied successfully
✓ Connection verified
```
```

**File: `.claude/skills/postgres-k8s-setup/scripts/deploy.sh`**
```bash
#!/bin/bash
set -e

echo "🚀 Deploying PostgreSQL to Kubernetes..."

# Add Bitnami Helm repo
helm repo add bitnami https://charts.bitnami.com/bitnami 2>/dev/null || true
helm repo update

# Create namespace
kubectl create namespace database --dry-run=client -o yaml | kubectl apply -f -

# Generate random password
PG_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)

# Install PostgreSQL
helm install postgresql bitnami/postgresql \
  --namespace database \
  --set auth.username=learnflow_user \
  --set auth.password="$PG_PASSWORD" \
  --set auth.database=learnflow \
  --set primary.persistence.enabled=false \
  --wait \
  --timeout 5m

echo "✓ PostgreSQL deployed to namespace 'database'"
echo "✓ Database: learnflow"
echo "✓ Username: learnflow_user"
echo "✓ Password stored in Secret: postgresql"
```

**File: `.claude/skills/postgres-k8s-setup/scripts/verify.py`**
```python
#!/usr/bin/env python3
"""Verify PostgreSQL deployment."""
import subprocess
import sys

def run_kubectl(args):
    """Run kubectl command."""
    result = subprocess.run(
        ["kubectl"] + args,
        capture_output=True,
        text=True
    )
    return result.stdout.strip(), result.returncode

def verify_postgresql():
    """Verify PostgreSQL is running and accessible."""
    # Check pod status
    stdout, code = run_kubectl([
        "get", "pods", "-n", "database",
        "-l", "app.kubernetes.io/name=postgresql",
        "-o", "jsonpath={.items[0].status.phase}"
    ])

    if code != 0 or stdout != "Running":
        print(f"✗ PostgreSQL pod not running (status: {stdout})")
        return False

    print("✓ PostgreSQL pod running")

    # Test connection
    test_query = "SELECT version();"
    stdout, code = run_kubectl([
        "exec", "-n", "database",
        "postgresql-0", "--",
        "psql", "-U", "learnflow_user", "-d", "learnflow",
        "-c", test_query
    ])

    if code != 0:
        print("✗ Connection test failed")
        return False

    print("✓ Connection verified")
    return True

if __name__ == "__main__":
    success = verify_postgresql()
    sys.exit(0 if success else 1)
```

---

### Phase 5: Application Skills (Day 3-4)
**Duration:** 8-10 hours
**Priority:** CRITICAL - Core LearnFlow functionality

#### Skill 5.1: fastapi-dapr-agent

This skill teaches agents how to create FastAPI microservices with Dapr integration.

**File: `.claude/skills/fastapi-dapr-agent/SKILL.md`**
```markdown
---
name: fastapi-dapr-agent
description: Create FastAPI microservices with Dapr sidecar integration
version: 1.0.0
---

# FastAPI + Dapr Agent Microservice

## When to Use
- Creating LearnFlow AI agent services
- Building event-driven microservices
- Need pub/sub, state management, or service invocation

## What It Does
- Scaffolds FastAPI project with Dapr
- Configures pub/sub for Kafka
- Sets up state store (PostgreSQL via Dapr)
- Creates Kubernetes manifests with Dapr annotations
- Includes health checks and observability

## Instructions

1. **Generate service scaffold:**
   ```bash
   python scripts/scaffold_service.py \
     --name triage-agent \
     --port 8001 \
     --pubsub kafka-pubsub \
     --statestore postgres-state
   ```

2. **Build and containerize:**
   ```bash
   bash scripts/build.sh triage-agent
   ```

3. **Deploy to Kubernetes:**
   ```bash
   bash scripts/deploy.sh triage-agent
   ```

## Service Structure
```
backend/<service-name>/
├── main.py                 # FastAPI app
├── agents/
│   └── agent.py           # AI agent logic
├── models/
│   └── schemas.py         # Pydantic models
├── dapr/
│   ├── pubsub.yaml        # Pub/Sub component
│   └── statestore.yaml    # State store component
├── k8s/
│   ├── deployment.yaml    # K8s deployment with Dapr
│   └── service.yaml       # K8s service
├── Dockerfile
└── requirements.txt
```

## Dapr Integration Points
- **Pub/Sub:** Subscribe to topics, publish events
- **State Management:** Persist agent state
- **Service Invocation:** Call other microservices
- **Secrets:** Access database credentials

## Validation
- [ ] Service responds to health check
- [ ] Dapr sidecar initialized
- [ ] Can publish/subscribe to Kafka topics
- [ ] State persisted to PostgreSQL

## Expected Output
```
✓ Service scaffolded: backend/triage-agent
✓ Docker image built: learnflow/triage-agent:latest
✓ Deployed to namespace: learnflow
✓ Dapr sidecar ready
✓ Health check passed: http://triage-agent:8001/health
```
```

**File: `.claude/skills/fastapi-dapr-agent/scripts/scaffold_service.py`**
```python
#!/usr/bin/env python3
"""Scaffold a FastAPI microservice with Dapr integration."""
import argparse
import os
from pathlib import Path

FASTAPI_MAIN_TEMPLATE = '''"""
{service_name} - LearnFlow AI Agent Microservice
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="{service_name}")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dapr configuration
DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
DAPR_URL = f"http://localhost:{{DAPR_HTTP_PORT}}"
PUBSUB_NAME = "{pubsub}"
STATE_STORE = "{statestore}"

class QueryRequest(BaseModel):
    user_id: str
    query: str
    context: dict = {{}}

class QueryResponse(BaseModel):
    response: str
    agent: str
    confidence: float

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {{"status": "healthy", "service": "{service_name}"}}

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process user query with AI agent."""
    logger.info(f"Processing query from user {{request.user_id}}")

    # TODO: Implement agent logic
    response = QueryResponse(
        response="This is a placeholder response",
        agent="{service_name}",
        confidence=0.95
    )

    # Publish event via Dapr
    await publish_event("query.processed", {{
        "user_id": request.user_id,
        "query": request.query,
        "response": response.response
    }})

    return response

async def publish_event(topic: str, data: dict):
    """Publish event to Kafka via Dapr."""
    async with httpx.AsyncClient() as client:
        url = f"{{DAPR_URL}}/v1.0/publish/{{PUBSUB_NAME}}/{{topic}}"
        try:
            await client.post(url, json=data)
            logger.info(f"Published event to {{topic}}")
        except Exception as e:
            logger.error(f"Failed to publish event: {{e}}")

@app.post("/dapr/subscribe")
async def subscribe():
    """Dapr subscription endpoint."""
    return [
        {{
            "pubsubname": PUBSUB_NAME,
            "topic": "query.received",
            "route": "/events/query-received"
        }}
    ]

@app.post("/events/query-received")
async def handle_query_event(event: dict):
    """Handle incoming query events."""
    logger.info(f"Received event: {{event}}")
    # Process event
    return {{"status": "ok"}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port={port})
'''

DOCKERFILE_TEMPLATE = '''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "{port}"]
'''

REQUIREMENTS_TEMPLATE = '''fastapi==0.104.1
uvicorn[standard]==0.24.0
httpx==0.25.1
pydantic==2.5.0
python-dotenv==1.0.0
'''

K8S_DEPLOYMENT_TEMPLATE = '''apiVersion: apps/v1
kind: Deployment
metadata:
  name: {service_name}
  namespace: learnflow
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {service_name}
  template:
    metadata:
      labels:
        app: {service_name}
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "{service_name}"
        dapr.io/app-port: "{port}"
        dapr.io/log-level: "info"
    spec:
      containers:
      - name: {service_name}
        image: learnflow/{service_name}:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: {port}
        env:
        - name: DAPR_HTTP_PORT
          value: "3500"
        - name: DAPR_GRPC_PORT
          value: "50001"
---
apiVersion: v1
kind: Service
metadata:
  name: {service_name}
  namespace: learnflow
spec:
  selector:
    app: {service_name}
  ports:
  - port: {port}
    targetPort: {port}
  type: ClusterIP
'''

def scaffold_service(name, port, pubsub, statestore):
    """Generate service files."""
    service_dir = Path(f"backend/{name}")
    service_dir.mkdir(parents=True, exist_ok=True)

    # Create main.py
    with open(service_dir / "main.py", "w") as f:
        f.write(FASTAPI_MAIN_TEMPLATE.format(
            service_name=name,
            port=port,
            pubsub=pubsub,
            statestore=statestore
        ))

    # Create Dockerfile
    with open(service_dir / "Dockerfile", "w") as f:
        f.write(DOCKERFILE_TEMPLATE.format(port=port))

    # Create requirements.txt
    with open(service_dir / "requirements.txt", "w") as f:
        f.write(REQUIREMENTS_TEMPLATE)

    # Create K8s directory
    k8s_dir = service_dir / "k8s"
    k8s_dir.mkdir(exist_ok=True)

    # Create deployment.yaml
    with open(k8s_dir / "deployment.yaml", "w") as f:
        f.write(K8S_DEPLOYMENT_TEMPLATE.format(
            service_name=name,
            port=port
        ))

    print(f"✓ Service scaffolded: {service_dir}")
    print(f"  - main.py: FastAPI app with Dapr")
    print(f"  - Dockerfile: Container image config")
    print(f"  - k8s/deployment.yaml: Kubernetes manifests")
    print(f"\nNext steps:")
    print(f"  1. cd {service_dir}")
    print(f"  2. Implement agent logic in main.py")
    print(f"  3. Build: docker build -t learnflow/{name}:latest .")
    print(f"  4. Deploy: kubectl apply -f k8s/")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--pubsub", default="kafka-pubsub")
    parser.add_argument("--statestore", default="postgres-state")

    args = parser.parse_args()
    scaffold_service(args.name, args.port, args.pubsub, args.statestore)
```

---

### Phase 6-10: Remaining Skills & LearnFlow Build

Due to length constraints, I'll provide the strategic approach for remaining phases:

**Phase 6: Frontend Skills (nextjs-k8s-deploy)**
- Scaffold Next.js app with TypeScript
- Monaco editor integration for code editing
- Kubernetes deployment with Nginx ingress
- Token cost: ~115 tokens

**Phase 7: Integration Skills**
- **mcp-code-execution:** Generic MCP wrapper with code execution
- **docusaurus-deploy:** Documentation site generation
- Token cost: ~195 tokens combined

**Phase 8: LearnFlow Build**
- Use ALL skills to build complete application
- Claude Code and Goose work from same `.claude/skills/`
- Zero manual coding - only skill refinement

**Phase 9: Cloud Deployment**
- ArgoCD for GitOps CD
- GitHub Actions for CI
- Deploy to Azure/GCP/Oracle

**Phase 10: Polish & Submit**
- Comprehensive documentation
- Demo video
- Submit to hackathon

---

## 🎯 Token Efficiency Tracking

| Phase | Traditional MCP | Skills + Scripts | Savings |
|-------|----------------|------------------|---------|
| Setup | 15k tokens | 100 tokens | 99.3% |
| Infrastructure | 35k tokens | 215 tokens | 99.4% |
| Application | 40k tokens | 350 tokens | 99.1% |
| Frontend | 25k tokens | 115 tokens | 99.5% |
| **TOTAL** | **115k tokens** | **780 tokens** | **99.3%** |

---

## 🚨 Risk Mitigation (Learning from Previous Hackathons)

### Issue 1: Bugs from Manual Coding
**Previous:** Developers wrote code → introduced bugs → debugging cycles
**Hackathon III:** Skills write code → validation scripts → consistent output

### Issue 2: High Token/Quota Usage
**Previous:** MCP servers loaded at startup → 50k+ tokens wasted
**Hackathon III:** Scripts execute externally → only results in context

### Issue 3: Integration Failures
**Previous:** Tight coupling between components
**Hackathon III:** Modular skills with clear contracts

### Issue 4: Cross-Agent Incompatibility
**Previous:** Claude-specific patterns didn't work on Goose
**Hackathon III:** AAIF-compliant skills tested on both

---

## 📊 Success Metrics

### Skill Quality
- [ ] Works on both Claude Code and Goose
- [ ] Single-prompt deployment (no manual intervention)
- [ ] Token cost < 150 per skill
- [ ] Validation scripts pass 100%

### LearnFlow Application
- [ ] All 6 AI agents functional
- [ ] Kafka event streaming operational
- [ ] PostgreSQL persistence working
- [ ] Frontend deployed with code editor
- [ ] End-to-end demo successful

### Evaluation Score Targets
- Skills Autonomy: 15/15 points
- Token Efficiency: 10/10 points
- Architecture: 18/20 points
- Cross-Agent: 5/5 points
- **Target Total:** 85/100 points (Top tier)

---

## 📅 Timeline

| Day | Hours | Focus | Deliverable |
|-----|-------|-------|-------------|
| 1 | 6h | Setup + Foundation | Environment ready, agents-md-gen working |
| 2 | 8h | Infrastructure | Kafka + PostgreSQL skills complete |
| 3 | 8h | Application Backend | FastAPI + Dapr agents running |
| 4 | 8h | Frontend | Next.js deployed with Monaco |
| 5 | 6h | Integration | MCP + Docusaurus complete |
| 6 | 8h | LearnFlow Build | Full app running locally |
| 7 | 6h | Cloud Deploy | ArgoCD + GitHub Actions |
| 8 | 4h | Polish & Submit | Documentation + Demo |

**Total:** 54 hours (~7 days at 8h/day)

---

## 🎓 Key Learnings to Apply

1. **Skills are the Product** - Judges test skills directly, not just the app
2. **Token Efficiency Wins** - 99%+ reduction via code execution pattern
3. **Autonomy is Critical** - Single prompt → deployed system
4. **Test on Both Agents** - Claude Code AND Goose must work
5. **Validate Everything** - Scripts should verify success automatically

---

## 📝 Next Actions

Run this roadmap validation:

```bash
# 1. Create roadmap tracker
mkdir -p .hackathon
cp HACKATHON_III_ROADMAP.md .hackathon/

# 2. Initialize progress tracking
cat > .hackathon/progress.json << 'EOF'
{
  "phases": {
    "phase1_setup": {"status": "pending", "completeness": 0},
    "phase2_repos": {"status": "pending", "completeness": 0},
    "phase3_foundation": {"status": "pending", "completeness": 0},
    "phase4_infrastructure": {"status": "pending", "completeness": 0},
    "phase5_application": {"status": "pending", "completeness": 0},
    "phase6_frontend": {"status": "pending", "completeness": 0},
    "phase7_integration": {"status": "pending", "completeness": 0},
    "phase8_learnflow": {"status": "pending", "completeness": 0},
    "phase9_cloud": {"status": "pending", "completeness": 0},
    "phase10_submit": {"status": "pending", "completeness": 0}
  },
  "token_usage": {
    "target": 1000,
    "current": 0,
    "savings_vs_traditional": "99%"
  }
}
EOF

echo "✅ Hackathon III Roadmap Created!"
echo "Next: Start with Phase 1 - Environment Setup"
```

---

**Remember:** The skills you build today will be reusable for years. Make them autonomous, token-efficient, and cross-agent compatible.

**Good luck! 🚀**
