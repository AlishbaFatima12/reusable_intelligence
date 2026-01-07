"""
Learning Analytics using Claude API

Generates personalized learning insights and detects when students struggle.
"""

import logging
import json
from typing import Dict, Any, List
from backend.shared.claude_client import ClaudeClient
from backend.agents.progress.models import StudentProgressState, LearningInsight

logger = logging.getLogger(__name__)


class LearningAnalytics:
    """Generates learning insights using Claude API"""

    # System prompt for learning insights
    INSIGHTS_PROMPT = """You are an expert educational data analyst specializing in personalized learning.

Your task is to analyze student learning progress and generate actionable insights.

**Analysis Guidelines**:
1. Identify strengths (topics with high mastery)
2. Identify weaknesses (topics with low mastery or many errors)
3. Provide specific, actionable recommendations
4. Celebrate milestones and progress
5. Suggest interventions for struggling areas

**Response Format** (JSON array of insights):
[
  {
    "insight_type": "strength|weakness|recommendation|milestone",
    "title": "<brief title>",
    "description": "<detailed description>",
    "action_items": ["action 1", "action 2"]
  }
]

Keep insights:
- Specific and actionable
- Encouraging and supportive
- Backed by data
- Focused on next steps
"""

    # System prompt for struggle detection
    STRUGGLE_PROMPT = """You are an expert educational psychologist specializing in identifying learning struggles.

Analyze student behavior patterns to detect if they are struggling.

**Struggle Indicators**:
- Repeated similar errors
- Multiple queries on the same topic
- Frustration language ("I don't understand", "This doesn't work")
- Giving up quickly
- Avoiding certain topics

**Response Format** (JSON):
{
  "is_struggling": true|false,
  "confidence": 0.0-1.0,
  "struggle_indicators": ["indicator 1", "indicator 2"],
  "suggested_interventions": ["intervention 1", "intervention 2"]
}

Be compassionate and focus on constructive support.
"""

    def __init__(self, claude_client: ClaudeClient):
        self.client = claude_client

    async def generate_insights(
        self,
        student_state: StudentProgressState
    ) -> List[LearningInsight]:
        """
        Generate personalized learning insights for a student

        Args:
            student_state: Current student progress state

        Returns:
            List of learning insights
        """
        # Build progress summary
        progress_summary = self._build_progress_summary(student_state)

        prompt = f"""Analyze this student's learning progress and generate 2-4 insights:

**Student Progress Summary**:
{progress_summary}

Provide insights as a JSON array following the specified format.
"""

        try:
            result = self.client.generate_response(
                prompt=prompt,
                system_prompt=self.INSIGHTS_PROMPT
            )

            response_text = result["response_text"].strip()

            # Parse JSON response
            if response_text.startswith("```json"):
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif response_text.startswith("```"):
                response_text = response_text.split("```")[1].split("```")[0].strip()

            insights_data = json.loads(response_text)

            # Convert to LearningInsight objects
            insights = []
            for insight in insights_data:
                insights.append(LearningInsight(
                    student_id=student_state.student_id,
                    insight_type=insight.get("insight_type", "recommendation"),
                    title=insight.get("title", "Learning Insight"),
                    description=insight.get("description", ""),
                    action_items=insight.get("action_items", []),
                    generated_at=student_state.last_active_timestamp
                ))

            logger.info(f"Generated {len(insights)} insights for student {student_state.student_id}")
            return insights

        except Exception as e:
            logger.error(f"Error generating insights: {e}", exc_info=True)
            return self._fallback_insights(student_state)

    async def detect_struggle(
        self,
        student_id: str,
        recent_queries: List[str],
        recent_errors: List[str]
    ) -> Dict[str, Any]:
        """
        Detect if student is struggling based on recent activity

        Args:
            student_id: Student identifier
            recent_queries: Recent query texts
            recent_errors: Recent error messages

        Returns:
            Struggle detection result
        """
        prompt = f"""Analyze this student's recent activity for signs of struggle:

**Recent Queries** ({len(recent_queries)} total):
{self._format_list(recent_queries[:10])}  # Limit to 10 most recent

**Recent Errors** ({len(recent_errors)} total):
{self._format_list(recent_errors[:5])}  # Limit to 5 most recent

Provide analysis as JSON following the specified format.
"""

        try:
            result = self.client.generate_response(
                prompt=prompt,
                system_prompt=self.STRUGGLE_PROMPT
            )

            response_text = result["response_text"].strip()

            # Parse JSON response
            if response_text.startswith("```json"):
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif response_text.startswith("```"):
                response_text = response_text.split("```")[1].split("```")[0].strip()

            struggle_data = json.loads(response_text)

            logger.info(
                f"Struggle detection for {student_id}: "
                f"is_struggling={struggle_data.get('is_struggling', False)}"
            )

            return struggle_data

        except Exception as e:
            logger.error(f"Error detecting struggle: {e}", exc_info=True)
            return self._fallback_struggle_detection(recent_queries, recent_errors)

    def _build_progress_summary(self, student_state: StudentProgressState) -> str:
        """Build text summary of student progress"""
        summary_parts = [
            f"Overall Mastery: {student_state.progress.overall_mastery:.1%}",
            f"Total Queries: {student_state.total_queries}",
            f"Success Rate: {self._calculate_success_rate(student_state):.1%}",
            "",
            "Topic Mastery:"
        ]

        for tm in student_state.progress.topic_mastery:
            summary_parts.append(
                f"  - {tm.topic}: {tm.mastery_level:.1%} ({tm.interactions_count} interactions)"
            )

        if student_state.struggling_topics:
            summary_parts.append("")
            summary_parts.append(f"Struggling Topics: {', '.join(student_state.struggling_topics)}")

        return "\n".join(summary_parts)

    def _calculate_success_rate(self, student_state: StudentProgressState) -> float:
        """Calculate overall success rate"""
        if student_state.total_queries == 0:
            return 0.0
        return student_state.total_successful_queries / student_state.total_queries

    def _format_list(self, items: List[str]) -> str:
        """Format list as numbered items"""
        if not items:
            return "(none)"
        return "\n".join([f"{i+1}. {item}" for i, item in enumerate(items)])

    def _fallback_insights(self, student_state: StudentProgressState) -> List[LearningInsight]:
        """Generate fallback insights when Claude API fails"""
        insights = []

        # Check for milestones
        if student_state.progress.overall_mastery >= 0.8:
            insights.append(LearningInsight(
                student_id=student_state.student_id,
                insight_type="milestone",
                title="Excellent Progress!",
                description=f"You've achieved {student_state.progress.overall_mastery:.1%} overall mastery. Keep up the great work!",
                action_items=["Continue practicing advanced topics"],
                generated_at=student_state.last_active_timestamp
            ))

        # Check for struggles
        if student_state.struggling_topics:
            insights.append(LearningInsight(
                student_id=student_state.student_id,
                insight_type="weakness",
                title="Focus Area Identified",
                description=f"You may benefit from additional practice with: {', '.join(student_state.struggling_topics)}",
                action_items=[f"Review {student_state.struggling_topics[0]} fundamentals"],
                generated_at=student_state.last_active_timestamp
            ))

        return insights

    def _fallback_struggle_detection(
        self,
        recent_queries: List[str],
        recent_errors: List[str]
    ) -> Dict[str, Any]:
        """Fallback struggle detection using simple heuristics"""
        # Simple heuristic: many errors or repeated similar queries
        is_struggling = len(recent_errors) > 3 or len(recent_queries) > 10

        return {
            "is_struggling": is_struggling,
            "confidence": 0.6,
            "struggle_indicators": [
                f"{len(recent_errors)} recent errors" if recent_errors else "No errors",
                f"{len(recent_queries)} recent queries"
            ],
            "suggested_interventions": [
                "Consider reviewing fundamentals",
                "Try breaking down the problem into smaller steps"
            ]
        }
