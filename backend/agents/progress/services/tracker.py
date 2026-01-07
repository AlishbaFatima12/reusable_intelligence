"""
Progress Tracker - Student Milestone and Topic Tracking

Tracks student progress through Python curriculum topics.
"""

import logging
import time
from typing import Dict, List, Optional
from backend.shared.models import TopicMastery, LearningProgress
from backend.agents.progress.models import StudentProgressState

logger = logging.getLogger(__name__)


class ProgressTracker:
    """Tracks student learning milestones and topic mastery"""

    # Python curriculum topics (from spec.md)
    CURRICULUM_TOPICS = [
        "variables-and-data-types",
        "control-flow",
        "functions",
        "data-structures",
        "object-oriented-programming",
        "file-io-and-exceptions",
        "modules-and-packages"
    ]

    # Mastery thresholds
    MASTERY_THRESHOLD = 0.8  # 80% mastery
    STRUGGLING_THRESHOLD = 0.4  # Below 40% indicates struggle

    def __init__(self):
        pass

    def update_topic_mastery(
        self,
        student_state: StudentProgressState,
        topic: str,
        interaction_type: str,
        success: bool
    ) -> StudentProgressState:
        """
        Update student's mastery for a specific topic

        Args:
            student_state: Current student progress state
            topic: Topic name (normalized)
            interaction_type: Type of interaction (query, success, error, hint_request)
            success: Was the interaction successful?

        Returns:
            Updated student progress state
        """
        # Normalize topic name
        topic_normalized = self._normalize_topic(topic)

        # Find or create topic mastery entry
        topic_mastery = None
        for tm in student_state.progress.topic_mastery:
            if tm.topic_name == topic_normalized:
                topic_mastery = tm
                break

        if not topic_mastery:
            # Create new topic mastery entry
            topic_mastery = TopicMastery(
                topic_name=topic_normalized,
                mastery_percentage=0.0,
                exercises_completed=0
            )
            student_state.progress.topic_mastery.append(topic_mastery)

        # Update interaction count
        topic_mastery.exercises_completed += 1

        # Calculate mastery delta based on interaction type and success
        # Convert mastery_percentage (0-100) to 0-1 scale for calculation
        current_mastery = topic_mastery.mastery_percentage / 100.0
        mastery_delta = self._calculate_mastery_delta(
            interaction_type=interaction_type,
            success=success,
            current_mastery=current_mastery
        )

        # Update mastery level (clamped between 0.0 and 100.0)
        new_mastery = max(0.0, min(1.0, current_mastery + mastery_delta))
        topic_mastery.mastery_percentage = new_mastery * 100.0

        # Check if student is struggling with this topic
        if topic_mastery.mastery_percentage / 100.0 < self.STRUGGLING_THRESHOLD:
            if topic_normalized not in student_state.struggling_topics:
                student_state.struggling_topics.append(topic_normalized)
                logger.warning(
                    f"Student {student_state.student_id} struggling with {topic_normalized}: "
                    f"mastery={topic_mastery.mastery_percentage:.2f}%"
                )
        else:
            # Remove from struggling list if mastery improved
            if topic_normalized in student_state.struggling_topics:
                student_state.struggling_topics.remove(topic_normalized)

        # Update overall mastery
        student_state.progress.overall_mastery = self._calculate_overall_mastery(
            student_state.progress.topic_mastery
        )

        # Update last active timestamp
        student_state.last_active_timestamp = int(time.time())

        logger.info(
            f"Updated mastery: student={student_state.student_id}, topic={topic_normalized}, "
            f"mastery={topic_mastery.mastery_percentage:.2f}%, overall={student_state.progress.overall_mastery:.2f}"
        )

        return student_state

    def get_next_recommended_topic(self, student_state: StudentProgressState) -> Optional[str]:
        """
        Recommend next topic to study based on current progress

        Strategy:
        1. If struggling with a topic, recommend resources for that topic
        2. If a topic is near mastery (>70%), recommend it to reach 80%
        3. Otherwise, recommend the next unstarted topic in curriculum order

        Args:
            student_state: Current student progress state

        Returns:
            Next recommended topic or None
        """
        # Check if student is struggling - recommend that topic
        if student_state.struggling_topics:
            return student_state.struggling_topics[0]

        # Find topics near mastery (70-80%)
        near_mastery_topics = [
            tm.topic_name for tm in student_state.progress.topic_mastery
            if 70.0 <= tm.mastery_percentage < self.MASTERY_THRESHOLD * 100.0
        ]
        if near_mastery_topics:
            return near_mastery_topics[0]

        # Find next unstarted topic in curriculum order
        started_topics = {tm.topic_name for tm in student_state.progress.topic_mastery}
        for topic in self.CURRICULUM_TOPICS:
            if topic not in started_topics:
                return topic

        # All topics started - recommend lowest mastery topic
        if student_state.progress.topic_mastery:
            lowest_mastery = min(
                student_state.progress.topic_mastery,
                key=lambda tm: tm.mastery_percentage
            )
            return lowest_mastery.topic_name

        # Default to first topic
        return self.CURRICULUM_TOPICS[0]

    def _calculate_mastery_delta(
        self,
        interaction_type: str,
        success: bool,
        current_mastery: float
    ) -> float:
        """
        Calculate change in mastery based on interaction

        Args:
            interaction_type: Type of interaction
            success: Was it successful?
            current_mastery: Current mastery level

        Returns:
            Mastery delta (-1.0 to 1.0)
        """
        # Base deltas
        if interaction_type == "query":
            delta = 0.05 if success else -0.02
        elif interaction_type == "success":
            delta = 0.1
        elif interaction_type == "error":
            delta = -0.05
        elif interaction_type == "hint_request":
            delta = 0.02  # Small positive for engagement
        else:
            delta = 0.01  # Default small positive

        # Scale delta based on current mastery (diminishing returns at high mastery)
        if current_mastery > 0.8:
            delta *= 0.5  # Harder to improve beyond 80%

        return delta

    def _calculate_overall_mastery(self, topic_mastery_list: List[TopicMastery]) -> float:
        """
        Calculate overall mastery as average of topic masteries

        Args:
            topic_mastery_list: List of topic mastery objects

        Returns:
            Overall mastery score (0.0-1.0)
        """
        if not topic_mastery_list:
            return 0.0

        # Convert mastery_percentage (0-100) to 0-1 scale and average
        total_mastery = sum(tm.mastery_percentage / 100.0 for tm in topic_mastery_list)
        return total_mastery / len(topic_mastery_list)

    def _normalize_topic(self, topic: str) -> str:
        """
        Normalize topic name to match curriculum topics

        Args:
            topic: Raw topic name

        Returns:
            Normalized topic name
        """
        topic_lower = topic.lower().replace(" ", "-")

        # Map common variations to curriculum topics
        topic_mappings = {
            "variables": "variables-and-data-types",
            "data-types": "variables-and-data-types",
            "if-else": "control-flow",
            "loops": "control-flow",
            "function": "functions",
            "lists": "data-structures",
            "dictionaries": "data-structures",
            "dicts": "data-structures",
            "oop": "object-oriented-programming",
            "classes": "object-oriented-programming",
            "files": "file-io-and-exceptions",
            "exceptions": "file-io-and-exceptions",
            "import": "modules-and-packages"
        }

        # Check if it maps to a known topic
        for key, mapped_topic in topic_mappings.items():
            if key in topic_lower:
                return mapped_topic

        # Check if it's already a curriculum topic
        if topic_lower in self.CURRICULUM_TOPICS:
            return topic_lower

        # Default to most general topic
        return "variables-and-data-types"
