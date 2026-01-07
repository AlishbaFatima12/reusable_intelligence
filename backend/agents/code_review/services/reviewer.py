"""
Code Reviewer using Claude API

Analyzes student code and provides constructive feedback.
"""

import logging
import json
from typing import Dict, Any, List
from backend.shared.claude_client import ClaudeClient
from backend.agents.code_review.models import CodeFeedback

logger = logging.getLogger(__name__)


class CodeReviewer:
    """Reviews code submissions using Claude API"""

    # System prompt for code review
    REVIEW_PROMPT = """You are an experienced programming instructor reviewing student code.

Your task is to provide constructive, educational feedback that helps students improve. Focus on:
- Code correctness and potential bugs
- Code style and readability
- Efficiency and optimization opportunities
- Best practices and design patterns
- Learning opportunities

**Response Format** (JSON):
{
  "overall_rating": "<excellent|good|needs_improvement|poor>",
  "feedback_items": [
    {
      "category": "<style|correctness|efficiency|best_practice>",
      "severity": "<info|warning|error>",
      "line_number": <int or null>,
      "message": "<feedback message>",
      "suggestion": "<suggested fix or improvement>"
    }
  ],
  "summary": "<overall assessment>",
  "strengths": ["strength 1", "strength 2"],
  "improvements": ["improvement 1", "improvement 2"]
}

**Guidelines**:
1. Be constructive and encouraging - focus on learning
2. Provide specific, actionable feedback with examples
3. Acknowledge what the student did well
4. Prioritize critical issues (errors) before style issues
5. Include code suggestions where applicable
6. Keep feedback appropriate for the student's level
"""

    def __init__(self, claude_client: ClaudeClient):
        self.client = claude_client

    async def review_code(
        self,
        code: str,
        language: str = "python",
        context: str = None
    ) -> Dict[str, Any]:
        """
        Review student code submission

        Args:
            code: The code to review
            language: Programming language
            context: What the code is supposed to do

        Returns:
            Code review feedback
        """
        # Build the prompt
        context_text = f"\n**Purpose**: {context}" if context else ""
        prompt = f"""Review the following {language} code submitted by a student:{context_text}

```{language}
{code}
```

Provide constructive feedback as a JSON object following the specified format.
Focus on helping the student learn and improve their programming skills.
"""

        try:
            # Call Claude API
            result = self.client.generate_response(
                prompt=prompt,
                system_prompt=self.REVIEW_PROMPT
            )

            response_text = result["response_text"].strip()

            # Parse JSON response
            if response_text.startswith("```json"):
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif response_text.startswith("```"):
                response_text = response_text.split("```")[1].split("```")[0].strip()

            review_data = json.loads(response_text)

            # Convert feedback items to CodeFeedback objects
            feedback_items = []
            for item in review_data.get("feedback_items", []):
                feedback_items.append(CodeFeedback(
                    category=item.get("category", "style"),
                    severity=item.get("severity", "info"),
                    line_number=item.get("line_number"),
                    message=item.get("message", ""),
                    suggestion=item.get("suggestion")
                ))

            return {
                "overall_rating": review_data.get("overall_rating", "good"),
                "feedback_items": feedback_items,
                "summary": review_data.get("summary", "Code reviewed successfully."),
                "strengths": review_data.get("strengths", []),
                "improvements": review_data.get("improvements", []),
                "processing_time_ms": result["processing_time_ms"],
                "token_count": result["token_count"]
            }

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Claude response as JSON: {e}")
            return self._fallback_review()

        except Exception as e:
            logger.error(f"Error reviewing code: {e}", exc_info=True)
            return self._fallback_review()

    def _fallback_review(self) -> Dict[str, Any]:
        """
        Simple fallback review when Claude API fails

        Returns a basic template review.
        """
        logger.warning("Using fallback code review")

        return {
            "overall_rating": "needs_improvement",
            "feedback_items": [
                CodeFeedback(
                    category="system",
                    severity="warning",
                    line_number=None,
                    message="Unable to complete automated review at this time. Please try again.",
                    suggestion="Retry the review request"
                )
            ],
            "summary": "Automated review temporarily unavailable. Please try again in a moment.",
            "strengths": [],
            "improvements": ["Retry code review when service is available"],
            "processing_time_ms": 0,
            "token_count": 0
        }
