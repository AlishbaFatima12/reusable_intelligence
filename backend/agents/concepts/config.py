"""
Concepts Agent Configuration

Loads environment-specific configuration for the Concepts Agent.
"""

from backend.shared.config import get_config

# Load Concepts-specific configuration
config = get_config("concepts")
