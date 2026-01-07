"""
Triage Agent Configuration

Loads environment-specific configuration for the Triage Agent.
"""

from backend.shared.config import get_config

# Load Triage-specific configuration
config = get_config("triage")
