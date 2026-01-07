# agents-md-gen

Auto-generates AGENTS.md documentation for FastAPI multi-agent microservice projects.

## Usage

```bash
python .claude/skills/agents-md-gen/scripts/main.py --backend-dir ./backend
```

## Options

- `--backend-dir`: Path to backend directory containing agent subdirectories (default: `./backend`)
- `--output`: Output path for AGENTS.md (default: `./AGENTS.md`)
- `--validate`: Run AAIF compliance validation after generation

## Output

Generates AAIF-compliant AGENTS.md with:
- Agent names, ports, purposes
- API endpoints with request/response schemas
- External dependencies
- Pub/Sub topics

Token-efficient validation: `✓ PASS` or `✗ FAIL: N issues`
