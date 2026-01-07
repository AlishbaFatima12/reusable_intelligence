"""
Debug Agent Configuration

Loads environment-specific configuration for the Debug Agent.
"""

from backend.shared.config import get_config

# Load Debug-specific configuration
config = get_config("debug")
