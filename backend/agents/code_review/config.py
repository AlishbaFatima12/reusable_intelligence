"""
Code Review Agent Configuration

Loads environment-specific configuration for the Code Review Agent.
"""

from backend.shared.config import get_config

# Load Code Review-specific configuration
config = get_config("code-review")
