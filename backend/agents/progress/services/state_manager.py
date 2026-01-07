"""
State Manager for Student Progress

Uses Dapr state store to persist student progress data.
"""

import logging
import time
from typing import Optional
from backend.shared.dapr_client import DaprStateClient
from backend.shared.models import LearningProgress, TopicMastery
from backend.agents.progress.models import StudentProgressState

logger = logging.getLogger(__name__)


class ProgressStateManager:
    """Manages student progress state using Dapr state store"""

    def __init__(self):
        self.state_client = DaprStateClient()

    def get_student_progress(self, student_id: str) -> StudentProgressState:
        """
        Retrieve student progress from state store

        Args:
            student_id: Student identifier

        Returns:
            Student progress state (creates new if not found)
        """
        state_key = self._get_state_key(student_id)

        try:
            state_data = self.state_client.get_state(state_key)

            if state_data:
                student_state = StudentProgressState(**state_data)
                logger.info(
                    f"Retrieved progress for student {student_id}: "
                    f"overall_mastery={student_state.progress.overall_mastery:.2f}"
                )
                return student_state

            # Create new progress state for new student
            logger.info(f"Creating new progress state for student {student_id}")
            return self._create_new_student_state(student_id)

        except Exception as e:
            logger.error(f"Error retrieving student progress: {e}")
            return self._create_new_student_state(student_id)

    def save_student_progress(self, student_state: StudentProgressState):
        """
        Save student progress to state store

        Args:
            student_state: Student progress state to save
        """
        state_key = self._get_state_key(student_state.student_id)

        try:
            self.state_client.save_state(
                key=state_key,
                value=student_state.model_dump()
                # No TTL - student progress persists indefinitely
            )

            logger.info(
                f"Saved progress for student {student_state.student_id}: "
                f"overall_mastery={student_state.progress.overall_mastery:.2f}, "
                f"topics={len(student_state.progress.topic_mastery)}"
            )

        except Exception as e:
            logger.error(f"Error saving student progress: {e}")
            raise

    def get_all_student_ids(self) -> list:
        """
        Get list of all student IDs with progress data

        Note: This is a placeholder - Dapr doesn't support listing all keys
        In production, maintain a separate index or use a database query

        Returns:
            List of student IDs
        """
        # TODO: Implement using a separate index or database query
        logger.warning("get_all_student_ids not implemented - returning empty list")
        return []

    def delete_student_progress(self, student_id: str):
        """
        Delete student progress (for testing or data cleanup)

        Args:
            student_id: Student identifier
        """
        state_key = self._get_state_key(student_id)

        try:
            self.state_client.delete_state(state_key)
            logger.info(f"Deleted progress for student {student_id}")
        except Exception as e:
            logger.error(f"Error deleting student progress: {e}")
            raise

    def _create_new_student_state(self, student_id: str) -> StudentProgressState:
        """
        Create new student progress state with default values

        Args:
            student_id: Student identifier

        Returns:
            New student progress state
        """
        return StudentProgressState(
            student_id=student_id,
            progress=LearningProgress(
                student_id=student_id,
                overall_mastery=0.0,
                topic_mastery=[]
            ),
            total_queries=0,
            total_successful_queries=0,
            last_active_timestamp=int(time.time()),
            struggling_topics=[]
        )

    def _get_state_key(self, student_id: str) -> str:
        """
        Generate state store key for student progress

        Args:
            student_id: Student identifier

        Returns:
            State store key
        """
        return f"student_progress:{student_id}"
