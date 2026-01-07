"""
Exercise Generator Configuration

Loads environment-specific configuration for the Exercise Generator Agent.
"""

from backend.shared.config import get_config

# Load Exercise Generator-specific configuration
config = get_config("exercise")
