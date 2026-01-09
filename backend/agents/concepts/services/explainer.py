"""
Concept Explainer using Claude API

Generates clear, beginner-friendly explanations of programming concepts.
"""

import logging
import json
from typing import Dict, Any, List, Optional
from backend.shared.claude_client import ClaudeClient
from backend.agents.concepts.models import CodeExample

logger = logging.getLogger(__name__)


class ConceptExplainer:
    """Explains programming concepts using Claude API"""

    # System prompt for concept explanations
    EXPLANATION_PROMPT = """You are an expert Python programming tutor specializing in clear, beginner-friendly explanations.

Your task is to explain programming concepts in a way that beginners can understand. Use:
- Simple language without jargon (or define jargon when necessary)
- Real-world analogies
- Code examples with comments
- ASCII visualizations where helpful
- Common mistakes to avoid

**Response Format** (JSON):
{
  "explanation": "<clear explanation>",
  "code_examples": [
    {
      "title": "<example name>",
      "code": "<python code with comments>",
      "explanation": "<what this demonstrates>"
    }
  ],
  "visualization": "<optional ASCII diagram>",
  "key_points": ["point 1", "point 2", "point 3"],
  "common_mistakes": ["mistake 1", "mistake 2"],
  "next_steps": "<suggested next learning steps>"
}

**Guidelines**:
1. Explanation should be 2-4 paragraphs
2. Include 2-3 code examples of increasing complexity
3. Keep code examples under 15 lines each
4. Use comments in code to explain key parts
5. ASCII visualizations should be simple and clear
6. Key points should be concise (1 sentence each)
7. Common mistakes should include why they're mistakes
"""

    def __init__(self, claude_client: ClaudeClient):
        self.client = claude_client

    async def explain_concept(
        self,
        concept: str,
        difficulty_level: str = "beginner",
        include_examples: bool = True,
        include_visualization: bool = True
    ) -> Dict[str, Any]:
        """
        Generate explanation for a programming concept

        Args:
            concept: The concept to explain (e.g., "recursion", "list comprehensions")
            difficulty_level: Target difficulty (beginner, intermediate, advanced)
            include_examples: Whether to include code examples
            include_visualization: Whether to include ASCII visualizations

        Returns:
            Explanation with code examples, visualizations, and key points
        """
        # Build the prompt
        prompt = f"""Explain the following Python programming concept to a {difficulty_level} learner:

**Concept**: {concept}

**Include**:
- Clear explanation with analogies
{"- Multiple code examples" if include_examples else ""}
{"- ASCII visualization or diagram" if include_visualization else ""}
- Key points to remember
- Common mistakes

Provide your response as a JSON object following the specified format.
"""

        try:
            # Call Claude API
            result = self.client.generate_response(
                prompt=prompt,
                system_prompt=self.EXPLANATION_PROMPT
            )

            response_text = result["response_text"].strip()

            # Parse JSON response
            if response_text.startswith("```json"):
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif response_text.startswith("```"):
                response_text = response_text.split("```")[1].split("```")[0].strip()

            # Parse JSON with strict=False to handle control characters
            explanation_data = json.loads(response_text, strict=False)

            # Convert code examples to CodeExample objects
            code_examples = []
            for ex in explanation_data.get("code_examples", []):
                code_examples.append(CodeExample(
                    title=ex.get("title", "Example"),
                    code=ex.get("code", ""),
                    explanation=ex.get("explanation", "")
                ))

            return {
                "explanation": explanation_data.get("explanation", ""),
                "code_examples": code_examples,
                "visualization": explanation_data.get("visualization"),
                "key_points": explanation_data.get("key_points", []),
                "common_mistakes": explanation_data.get("common_mistakes", []),
                "next_steps": explanation_data.get("next_steps"),
                "processing_time_ms": result["processing_time_ms"],
                "token_count": result["token_count"]
            }

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Claude response as JSON: {e}")
            logger.debug(f"Raw response (first 500 chars): {response_text[:500]}")
            # Try to extract plain text explanation if JSON parsing fails
            return {
                "explanation": response_text if len(response_text) < 2000 else response_text[:2000],
                "code_examples": [],
                "visualization": None,
                "key_points": [],
                "common_mistakes": [],
                "next_steps": "Practice writing Python code",
                "processing_time_ms": result.get("processing_time_ms", 0),
                "token_count": result.get("token_count", 0)
            }

        except Exception as e:
            logger.error(f"Error generating explanation: {e}", exc_info=True)
            return self._fallback_explanation(concept, difficulty_level)

    def _fallback_explanation(self, concept: str, difficulty_level: str) -> Dict[str, Any]:
        """
        Simple fallback explanation when Claude API fails

        Returns a basic template explanation.
        """
        logger.warning(f"Using fallback explanation for: {concept}")

        return {
            "explanation": f"{concept} is an important Python programming concept that allows you to write more efficient and elegant code. Due to a temporary issue, we're unable to provide a detailed explanation right now. Please try again in a moment.",
            "code_examples": [],
            "visualization": None,
            "key_points": [
                f"Understanding {concept} is important for Python programming",
                "Try again for a detailed explanation"
            ],
            "common_mistakes": [],
            "next_steps": "Retry this request or consult Python documentation",
            "processing_time_ms": 0,
            "token_count": 0
        }
