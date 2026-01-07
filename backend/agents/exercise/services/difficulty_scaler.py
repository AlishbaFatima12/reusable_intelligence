"""
Difficulty Scaler

Adjusts exercise difficulty based on student mastery level.
"""

import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class DifficultyScaler:
    """
    Adjust exercise difficulty based on student mastery and performance
    """

    # Mastery thresholds for auto-scaling
    BEGINNER_THRESHOLD = 0.3
    INTERMEDIATE_THRESHOLD = 0.6
    ADVANCED_THRESHOLD = 0.85

    def __init__(self):
        pass

    def recommend_difficulty(
        self,
        mastery_score: Optional[float] = None,
        requested_difficulty: str = "beginner"
    ) -> str:
        """
        Recommend difficulty level based on mastery score

        Args:
            mastery_score: Student's current mastery (0.0-1.0)
            requested_difficulty: Student's requested difficulty

        Returns:
            Recommended difficulty level
        """
        # If no mastery score, use requested difficulty
        if mastery_score is None:
            return requested_difficulty

        # Auto-scale based on mastery
        if mastery_score < self.BEGINNER_THRESHOLD:
            return "beginner"
        elif mastery_score < self.INTERMEDIATE_THRESHOLD:
            return "intermediate"
        elif mastery_score < self.ADVANCED_THRESHOLD:
            return "advanced"
        else:
            return "expert"

    def get_exercise_parameters(
        self,
        difficulty: str,
        topic: str
    ) -> Dict:
        """
        Get exercise generation parameters based on difficulty

        Returns:
            Dictionary with parameters for exercise generation
        """
        base_params = {
            "topic": topic,
            "difficulty": difficulty
        }

        if difficulty == "beginner":
            return {
                **base_params,
                "complexity": "simple",
                "code_length": "short (5-10 lines)",
                "concepts": "single concept",
                "hints_count": 3,
                "example_provided": True
            }
        elif difficulty == "intermediate":
            return {
                **base_params,
                "complexity": "moderate",
                "code_length": "medium (10-20 lines)",
                "concepts": "2-3 concepts",
                "hints_count": 2,
                "example_provided": False
            }
        elif difficulty == "advanced":
            return {
                **base_params,
                "complexity": "challenging",
                "code_length": "longer (20-40 lines)",
                "concepts": "multiple concepts",
                "hints_count": 1,
                "example_provided": False
            }
        else:  # expert
            return {
                **base_params,
                "complexity": "expert-level",
                "code_length": "unrestricted",
                "concepts": "multiple advanced concepts",
                "hints_count": 0,
                "example_provided": False
            }

    def suggest_next_topics(
        self,
        current_topic: str,
        mastery_score: Optional[float] = None
    ) -> list[str]:
        """
        Suggest next topics based on current topic and mastery

        Args:
            current_topic: Current topic being studied
            mastery_score: Mastery level of current topic

        Returns:
            List of suggested next topics
        """
        # Topic progression map
        topic_map = {
            "variables": ["data types", "operators", "basic input/output"],
            "data types": ["type conversion", "strings", "numbers"],
            "operators": ["conditionals", "boolean logic"],
            "conditionals": ["loops", "control flow"],
            "loops": ["functions", "lists"],
            "lists": ["list comprehensions", "tuples", "dictionaries"],
            "dictionaries": ["sets", "data structures"],
            "functions": ["parameters and arguments", "return values", "scope"],
            "scope": ["closures", "decorators", "lambda functions"],
            "strings": ["string methods", "formatting", "regular expressions"],
            "file io": ["error handling", "context managers"],
            "error handling": ["exceptions", "debugging"],
            "classes": ["object-oriented programming", "inheritance"],
            "inheritance": ["polymorphism", "encapsulation"],
            "modules": ["packages", "imports"],
        }

        # Get next topics from map
        next_topics = topic_map.get(current_topic.lower(), [])

        # If mastery is high, suggest more advanced topics
        if mastery_score and mastery_score > 0.8 and next_topics:
            return next_topics[:2]  # Top 2 next topics

        return next_topics[:3] if next_topics else ["Keep practicing current topic"]
