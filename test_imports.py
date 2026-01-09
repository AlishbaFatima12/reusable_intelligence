#!/usr/bin/env python
"""Test if agent imports work without Dapr daemon"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing imports...")
print("=" * 50)

try:
    print("\n1. Testing backend.shared.dapr_client...")
    from backend.shared.dapr_client import DaprStateClient, DaprPubSubClient
    print("   [OK] DaprStateClient and DaprPubSubClient imported")

    # Test instantiation
    state_client = DaprStateClient()
    print("   [OK] DaprStateClient instantiated")

    pubsub_client = DaprPubSubClient()
    print("   [OK] DaprPubSubClient instantiated")

except Exception as e:
    print(f"   [FAIL] {e}")
    import traceback
    traceback.print_exc()

try:
    print("\n2. Testing triage agent...")
    from backend.agents.triage.main import app
    print("   [OK] Triage agent imported successfully")
except Exception as e:
    print(f"   [FAIL] {e}")
    import traceback
    traceback.print_exc()

try:
    print("\n3. Testing concepts agent...")
    from backend.agents.concepts.main import app
    print("   [OK] Concepts agent imported successfully")
except Exception as e:
    print(f"   [FAIL] {e}")
    import traceback
    traceback.print_exc()

try:
    print("\n4. Testing progress agent...")
    from backend.agents.progress.main import app
    print("   [OK] Progress agent imported successfully")
except Exception as e:
    print(f"   [FAIL] {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("Import test complete!")
