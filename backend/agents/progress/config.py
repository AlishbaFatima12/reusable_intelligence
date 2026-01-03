"""
Progress Tracker Agent Configuration

Loads environment-specific configuration for the Progress Tracker Agent.
"""

from backend.shared.config import get_config

# Load Progress-specific configuration
config = get_config("progress")
