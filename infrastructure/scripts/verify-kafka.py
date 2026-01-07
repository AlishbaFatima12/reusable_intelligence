#!/usr/bin/env python3
"""Verify Kafka topics are created"""

import sys
import json
from kafka import KafkaAdminClient
from kafka.errors import KafkaError

EXPECTED_TOPICS = [
    "student-queries",
    "triage-routing",
    "agent-responses",
    "student-struggle",
    "mastery-updates",
    "agent-logs",
    "agent-status",
]

def main():
    """Check Kafka topics"""
    try:
        admin_client = KafkaAdminClient(
            bootstrap_servers="localhost:9092",
            request_timeout_ms=5000
        )

        existing_topics = admin_client.list_topics()
        found_topics = [t for t in EXPECTED_TOPICS if t in existing_topics]

        # Minimal output (~10 tokens)
        output = {
            "topics": len(found_topics),
            "expected": len(EXPECTED_TOPICS),
            "status": "ready" if len(found_topics) == len(EXPECTED_TOPICS) else "incomplete"
        }

        print(json.dumps(output))
        sys.exit(0 if len(found_topics) == len(EXPECTED_TOPICS) else 1)

    except KafkaError as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
