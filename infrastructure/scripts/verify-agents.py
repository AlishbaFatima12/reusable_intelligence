#!/usr/bin/env python3
"""Verify all LearnFlow agents are healthy"""

import sys
import httpx
import json

AGENTS = {
    "triage": 8001,
    "concepts": 8002,
    "code-review": 8003,
    "debug": 8004,
    "exercise": 8005,
    "progress": 8006,
}

def check_agent(name, port):
    """Check if agent is healthy"""
    try:
        response = httpx.get(f"http://localhost:{port}/health", timeout=5.0)
        return response.status_code == 200
    except Exception:
        return False

def main():
    """Check all agents"""
    results = {}
    all_healthy = True

    for name, port in AGENTS.items():
        healthy = check_agent(name, port)
        results[name] = "healthy" if healthy else "unhealthy"
        if not healthy:
            all_healthy = False

    # Minimal output (~10 tokens)
    output = {
        "status": "healthy" if all_healthy else "degraded",
        "agents": len([v for v in results.values() if v == "healthy"]),
        "total": len(AGENTS)
    }

    print(json.dumps(output))
    sys.exit(0 if all_healthy else 1)

if __name__ == "__main__":
    main()
