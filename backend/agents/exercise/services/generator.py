"""
Exercise Generator Service

Uses Claude API to generate practice exercises tailored to student level.
"""

import logging
import uuid
from typing import Dict, List, Optional
from backend.shared.claude_client import ClaudeClient
from backend.agents.exercise.services.difficulty_scaler import DifficultyScaler
from backend.agents.exercise.models import Exercise, TestCase

logger = logging.getLogger(__name__)


class ExerciseGenerator:
    """
    Generate practice exercises using Claude API
    """

    def __init__(self, claude_client: ClaudeClient):
        """
        Initialize ExerciseGenerator

        Args:
            claude_client: ClaudeClient instance for API calls
        """
        self.claude_client = claude_client
        self.difficulty_scaler = DifficultyScaler()

    async def generate_exercises(
        self,
        topic: str,
        difficulty_level: str = "beginner",
        count: int = 3,
        include_test_cases: bool = True,
        mastery_score: Optional[float] = None
    ) -> Dict:
        """
        Generate practice exercises for a given topic

        Args:
            topic: Topic for exercises
            difficulty_level: Difficulty level
            count: Number of exercises to generate
            include_test_cases: Whether to include test cases
            mastery_score: Current mastery score for difficulty scaling

        Returns:
            Dictionary with generated exercises
        """
        try:
            # Adjust difficulty based on mastery
            recommended_difficulty = self.difficulty_scaler.recommend_difficulty(
                mastery_score=mastery_score,
                requested_difficulty=difficulty_level
            )

            # Get exercise parameters
            params = self.difficulty_scaler.get_exercise_parameters(
                difficulty=recommended_difficulty,
                topic=topic
            )

            # Build prompt for Claude
            prompt = self._build_generation_prompt(
                topic=topic,
                difficulty=recommended_difficulty,
                count=count,
                include_test_cases=include_test_cases,
                params=params
            )

            # Call Claude API
            response = await self.claude_client.generate(prompt=prompt)

            # Parse response
            exercises_data = self._parse_exercises_response(
                response=response,
                topic=topic,
                difficulty=recommended_difficulty
            )

            # Add next topic suggestions
            next_topics = self.difficulty_scaler.suggest_next_topics(
                current_topic=topic,
                mastery_score=mastery_score
            )

            return {
                "exercises": exercises_data,
                "next_topic_suggestions": next_topics,
                "recommended_difficulty": recommended_difficulty
            }

        except Exception as e:
            logger.error(f"Error generating exercises: {e}", exc_info=True)
            return {
                "exercises": [],
                "next_topic_suggestions": [],
                "recommended_difficulty": difficulty_level
            }

    def _build_generation_prompt(
        self,
        topic: str,
        difficulty: str,
        count: int,
        include_test_cases: bool,
        params: Dict
    ) -> str:
        """
        Build prompt for Claude API to generate exercises
        """
        prompt = f"""You are an expert programming instructor creating practice exercises for students.

Topic: {topic}
Difficulty Level: {difficulty}
Number of Exercises: {count}

Exercise Parameters:
- Complexity: {params['complexity']}
- Expected Code Length: {params['code_length']}
- Concepts to Cover: {params['concepts']}
- Number of Hints: {params['hints_count']}
- Provide Example: {params['example_provided']}

Create {count} progressively challenging programming exercises for {topic}.

For each exercise, provide:

1. TITLE: A clear, engaging title
2. DESCRIPTION: Problem description with requirements (2-4 sentences)
3. LEARNING OBJECTIVES: 2-3 specific learning objectives
4. STARTER CODE: A code template to help students start (if appropriate for difficulty level)
5. HINTS: {params['hints_count']} progressive hints (start vague, get more specific)
"""

        if include_test_cases:
            prompt += """6. TEST CASES: 3-4 test cases with:
   - Input
   - Expected output
   - Brief explanation of what the test checks
"""

        prompt += """
Format your response as JSON array:
[
  {
    "title": "...",
    "description": "...",
    "learning_objectives": ["...", "..."],
    "starter_code": "...",
    "hints": ["...", "...", "..."],
    "test_cases": [
      {
        "input": "...",
        "expected_output": "...",
        "explanation": "..."
      }
    ]
  }
]

Make exercises practical, engaging, and appropriate for {difficulty} level students.
"""

        return prompt

    def _parse_exercises_response(
        self,
        response: str,
        topic: str,
        difficulty: str
    ) -> List[Exercise]:
        """
        Parse Claude's response into Exercise objects
        """
        try:
            import json

            # Extract JSON from response
            json_match = response.strip()
            if json_match.startswith("```json"):
                json_match = json_match[7:]
            if json_match.startswith("```"):
                json_match = json_match[3:]
            if json_match.endswith("```"):
                json_match = json_match[:-3]

            exercises_data = json.loads(json_match.strip())

            # Convert to Exercise objects
            exercises = []
            for i, ex_data in enumerate(exercises_data):
                # Generate unique exercise ID
                exercise_id = f"{topic.lower().replace(' ', '-')}-{difficulty}-{uuid.uuid4().hex[:8]}"

                # Parse test cases
                test_cases = []
                if "test_cases" in ex_data:
                    for tc in ex_data["test_cases"]:
                        test_cases.append(TestCase(
                            input=tc.get("input", ""),
                            expected_output=tc.get("expected_output", ""),
                            explanation=tc.get("explanation")
                        ))

                exercise = Exercise(
                    exercise_id=exercise_id,
                    title=ex_data.get("title", f"Exercise {i+1}"),
                    description=ex_data.get("description", ""),
                    difficulty=difficulty,
                    starter_code=ex_data.get("starter_code"),
                    test_cases=test_cases,
                    hints=ex_data.get("hints", []),
                    learning_objectives=ex_data.get("learning_objectives", [])
                )

                exercises.append(exercise)

            return exercises

        except Exception as e:
            logger.error(f"Error parsing exercises response: {e}", exc_info=True)
            return []
