"""
Debugger Service

Uses Claude API to analyze errors and provide debugging guidance.
"""

import logging
from typing import Dict, Optional, List
from backend.shared.claude_client import ClaudeClient
from backend.agents.debug.services.error_parser import ErrorParser
from backend.agents.debug.models import DiagnosticStep

logger = logging.getLogger(__name__)


class Debugger:
    """
    Analyze errors and provide debugging guidance using Claude API
    """

    def __init__(self, claude_client: ClaudeClient):
        """
        Initialize Debugger

        Args:
            claude_client: ClaudeClient instance for API calls
        """
        self.claude_client = claude_client
        self.error_parser = ErrorParser()

    async def diagnose_error(
        self,
        error_message: str,
        stack_trace: Optional[str] = None,
        code_snippet: Optional[str] = None,
        language: str = "python"
    ) -> Dict:
        """
        Diagnose error and provide debugging guidance

        Args:
            error_message: Error message or exception text
            stack_trace: Full stack trace (optional)
            code_snippet: Code that caused the error (optional)
            language: Programming language

        Returns:
            Dictionary with diagnosis results
        """
        try:
            # Parse error first
            parsed_error = self.error_parser.parse_error(
                error_message=error_message,
                stack_trace=stack_trace,
                language=language
            )

            error_category = self.error_parser.classify_error_category(
                parsed_error["error_type"]
            )

            # Build prompt for Claude
            prompt = self._build_diagnosis_prompt(
                error_message=error_message,
                error_type=parsed_error["error_type"],
                error_category=error_category,
                stack_trace=stack_trace,
                code_snippet=code_snippet,
                language=language
            )

            # Call Claude API
            result = self.claude_client.generate_response(prompt=prompt)
            response = result.get("response_text", "")

            # Parse Claude's response
            diagnosis = self._parse_diagnosis_response(
                response=response,
                error_type=parsed_error["error_type"],
                error_category=error_category
            )

            return diagnosis

        except Exception as e:
            logger.error(f"Error diagnosing error: {e}", exc_info=True)
            # Return fallback response
            return {
                "error_type": "unknown",
                "root_cause": "Unable to diagnose error",
                "explanation": f"Error analysis failed: {str(e)}",
                "diagnostic_steps": [],
                "suggested_fix": None,
                "learning_resources": []
            }

    def _build_diagnosis_prompt(
        self,
        error_message: str,
        error_type: str,
        error_category: str,
        stack_trace: Optional[str],
        code_snippet: Optional[str],
        language: str
    ) -> str:
        """
        Build prompt for Claude API to diagnose error
        """
        prompt = f"""You are a debugging assistant helping a student understand and fix their code error.

Programming Language: {language}
Error Type: {error_type}
Error Category: {error_category}

Error Message:
{error_message}
"""

        if stack_trace:
            prompt += f"""
Stack Trace:
{stack_trace}
"""

        if code_snippet:
            prompt += f"""
Code Snippet:
```{language}
{code_snippet}
```
"""

        prompt += """
Please provide:

1. ROOT CAUSE: What is the likely root cause of this error? (1-2 sentences)

2. EXPLANATION: Explain what went wrong in simple terms for a student learning programming. (2-3 sentences)

3. DIAGNOSTIC STEPS: Provide 3-5 numbered steps the student should follow to debug this issue. For each step, include:
   - Description: What to check or try
   - Reason: Why this step is important
   - Example: Example code or command (if applicable)

4. SUGGESTED FIX: Provide corrected code or specific changes to fix the error (if applicable)

5. LEARNING RESOURCES: Suggest 1-2 topics the student should learn more about (e.g., "Python exception handling", "List indexing")

Format your response as JSON:
{
  "root_cause": "...",
  "explanation": "...",
  "diagnostic_steps": [
    {
      "step_number": 1,
      "description": "...",
      "reason": "...",
      "example": "..."
    }
  ],
  "suggested_fix": "...",
  "learning_resources": ["...", "..."]
}
"""

        return prompt

    def _parse_diagnosis_response(
        self,
        response: str,
        error_type: str,
        error_category: str
    ) -> Dict:
        """
        Parse Claude's diagnosis response into structured format
        """
        try:
            import json

            # Try to extract JSON from response
            json_match = response.strip()
            if json_match.startswith("```json"):
                json_match = json_match[7:]
            if json_match.startswith("```"):
                json_match = json_match[3:]
            if json_match.endswith("```"):
                json_match = json_match[:-3]

            diagnosis = json.loads(json_match.strip())

            # Ensure required fields exist
            diagnosis.setdefault("root_cause", "Unknown")
            diagnosis.setdefault("explanation", "Unable to provide explanation")
            diagnosis.setdefault("diagnostic_steps", [])
            diagnosis.setdefault("suggested_fix", None)
            diagnosis.setdefault("learning_resources", [])

            # Add error type and category
            diagnosis["error_type"] = error_category

            return diagnosis

        except Exception as e:
            logger.error(f"Error parsing diagnosis response: {e}", exc_info=True)

            # Fallback: use raw response
            return {
                "error_type": error_category,
                "root_cause": error_type,
                "explanation": response[:500],  # First 500 chars
                "diagnostic_steps": [],
                "suggested_fix": None,
                "learning_resources": []
            }
