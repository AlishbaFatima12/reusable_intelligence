"""
Query Intent Classification using Claude API

Analyzes student queries to determine intent and extract entities.
"""

import logging
import json
from typing import Dict, Any, Optional
from backend.shared.claude_client import ClaudeClient
from backend.shared.models import IntentType

logger = logging.getLogger(__name__)


class IntentClassifier:
    """Classifies student queries using Claude API"""

    # System prompt for intent classification
    CLASSIFICATION_PROMPT = """You are an expert educational AI assistant specializing in Python programming education.

Your task is to analyze student queries and classify their intent into one of these categories:

1. **CONCEPT_EXPLANATION**: Student wants to understand a programming concept
   - Examples: "What is recursion?", "Explain how decorators work"

2. **CODE_REVIEW**: Student wants feedback on their code
   - Examples: "Is this code correct?", "How can I improve this function?"

3. **DEBUGGING**: Student has an error or bug to fix
   - Examples: "Why am I getting IndexError?", "My code doesn't run"

4. **EXERCISE_REQUEST**: Student wants practice problems
   - Examples: "Give me a problem on loops", "I need practice with lists"

5. **GENERAL_QUESTION**: General question about programming or learning
   - Examples: "What should I learn next?", "How long does it take to learn Python?"

Respond with a JSON object containing:
{
  "intent": "<INTENT_TYPE>",
  "confidence": <0.0-1.0>,
  "reasoning": "<brief explanation>",
  "entities": {
    "topics": ["topic1", "topic2"],
    "concepts": ["concept1"],
    "difficulty": "beginner|intermediate|advanced"
  },
  "routed_to_agent": "<agent-name>"
}

Agent routing rules:
- CONCEPT_EXPLANATION → "concepts-agent"
- CODE_REVIEW → "code-review-agent"
- DEBUGGING → "debug-agent"
- EXERCISE_REQUEST → "exercise-generator-agent"
- GENERAL_QUESTION → "concepts-agent" (default)
"""

    def __init__(self, claude_client: ClaudeClient):
        self.client = claude_client

    async def classify_query(
        self,
        query_text: str,
        code_snippet: Optional[str] = None,
        learning_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Classify student query intent using Claude API

        Args:
            query_text: The student's question
            code_snippet: Optional code snippet provided
            learning_context: Current learning context (topic, lesson)

        Returns:
            Classification result with intent, confidence, entities
        """
        # Build the prompt with context
        prompt_parts = [f"Student Query: {query_text}"]

        if code_snippet:
            prompt_parts.append(f"\nCode Snippet:\n```python\n{code_snippet}\n```")

        if learning_context:
            prompt_parts.append(f"\nLearning Context: {learning_context}")

        prompt = "\n".join(prompt_parts)

        try:
            # Call Claude API
            result = self.client.generate_response(
                prompt=prompt,
                system_prompt=self.CLASSIFICATION_PROMPT
            )

            response_text = result["response_text"].strip()

            # Parse JSON response
            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif response_text.startswith("```"):
                response_text = response_text.split("```")[1].split("```")[0].strip()

            classification = json.loads(response_text)

            # Validate and normalize intent
            intent_str = classification.get("intent", "GENERAL_QUESTION").upper()
            try:
                intent = IntentType(intent_str)
            except ValueError:
                logger.warning(f"Unknown intent '{intent_str}', defaulting to GENERAL_QUESTION")
                intent = IntentType.GENERAL_QUESTION

            return {
                "intent": intent,
                "confidence": classification.get("confidence", 0.5),
                "reasoning": classification.get("reasoning", ""),
                "entities": classification.get("entities", {}),
                "routed_to_agent": classification.get("routed_to_agent", "concepts-agent"),
                "processing_time_ms": result["processing_time_ms"],
                "token_count": result["token_count"]
            }

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Claude response as JSON: {e}")
            # Fallback classification
            return self._fallback_classification(query_text, code_snippet)

        except Exception as e:
            logger.error(f"Classification error: {e}")
            return self._fallback_classification(query_text, code_snippet)

    def _fallback_classification(
        self,
        query_text: str,
        code_snippet: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Simple rule-based fallback classification when Claude API fails

        Uses keyword matching as a backup strategy.
        """
        query_lower = query_text.lower()

        # Rule-based classification
        if any(word in query_lower for word in ["error", "bug", "wrong", "doesn't work", "traceback"]):
            intent = IntentType.DEBUGGING
            agent = "debug-agent"
        elif any(word in query_lower for word in ["review", "feedback", "improve", "check my code"]):
            intent = IntentType.CODE_REVIEW
            agent = "code-review-agent"
        elif any(word in query_lower for word in ["practice", "exercise", "problem", "challenge"]):
            intent = IntentType.EXERCISE_REQUEST
            agent = "exercise-generator-agent"
        elif any(word in query_lower for word in ["what is", "explain", "how does", "why"]):
            intent = IntentType.CONCEPT_EXPLANATION
            agent = "concepts-agent"
        else:
            intent = IntentType.GENERAL_QUESTION
            agent = "concepts-agent"

        logger.info(f"Used fallback classification: {intent.value} -> {agent}")

        return {
            "intent": intent,
            "confidence": 0.6,  # Lower confidence for rule-based
            "reasoning": "Fallback rule-based classification",
            "entities": {},
            "routed_to_agent": agent,
            "processing_time_ms": 0,
            "token_count": 0
        }
