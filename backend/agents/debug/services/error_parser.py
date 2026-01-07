"""
Error Parser

Parses stack traces and error messages to extract structured information.
"""

import re
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class ErrorParser:
    """
    Parse error messages and stack traces to extract structured information
    """

    # Common error patterns
    PYTHON_ERROR_PATTERN = re.compile(r'(\w+Error): (.+)')
    LINE_NUMBER_PATTERN = re.compile(r'line (\d+)')
    FILE_PATH_PATTERN = re.compile(r'File "([^"]+)"')

    def __init__(self):
        pass

    def parse_error(
        self,
        error_message: str,
        stack_trace: Optional[str] = None,
        language: str = "python"
    ) -> Dict:
        """
        Parse error message and stack trace into structured data

        Args:
            error_message: The error message or exception text
            stack_trace: Full stack trace (optional)
            language: Programming language

        Returns:
            Dictionary with parsed error information
        """
        try:
            parsed = {
                "error_type": self._extract_error_type(error_message, language),
                "error_message": error_message.strip(),
                "line_numbers": [],
                "file_paths": [],
                "trace_frames": []
            }

            # Parse stack trace if provided
            if stack_trace:
                parsed.update(self._parse_stack_trace(stack_trace, language))

            return parsed

        except Exception as e:
            logger.error(f"Error parsing error message: {e}", exc_info=True)
            return {
                "error_type": "unknown",
                "error_message": error_message,
                "line_numbers": [],
                "file_paths": [],
                "trace_frames": []
            }

    def _extract_error_type(self, error_message: str, language: str) -> str:
        """
        Extract the error type from error message

        Examples:
            "NameError: name 'x' is not defined" -> "NameError"
            "SyntaxError: invalid syntax" -> "SyntaxError"
        """
        if language == "python":
            match = self.PYTHON_ERROR_PATTERN.search(error_message)
            if match:
                return match.group(1)

        # Generic extraction - look for words ending in "Error" or "Exception"
        error_words = re.findall(r'\b(\w*(?:Error|Exception))\b', error_message)
        if error_words:
            return error_words[0]

        return "unknown"

    def _parse_stack_trace(self, stack_trace: str, language: str) -> Dict:
        """
        Parse stack trace into structured frames

        Returns:
            Dictionary with line_numbers, file_paths, trace_frames
        """
        lines = stack_trace.split('\n')
        frames = []
        line_numbers = []
        file_paths = []

        for i, line in enumerate(lines):
            # Extract file paths
            file_match = self.FILE_PATH_PATTERN.search(line)
            if file_match:
                file_path = file_match.group(1)
                file_paths.append(file_path)

            # Extract line numbers
            line_match = self.LINE_NUMBER_PATTERN.search(line)
            if line_match:
                line_num = int(line_match.group(1))
                line_numbers.append(line_num)

            # Build trace frames
            if file_match and line_match:
                # Look ahead for the actual code line
                code_line = ""
                if i + 1 < len(lines):
                    code_line = lines[i + 1].strip()

                frames.append({
                    "file": file_match.group(1),
                    "line": int(line_match.group(1)),
                    "code": code_line
                })

        return {
            "line_numbers": line_numbers,
            "file_paths": file_paths,
            "trace_frames": frames
        }

    def classify_error_category(self, error_type: str) -> str:
        """
        Classify error into broad categories

        Categories:
            - syntax: Code syntax issues
            - runtime: Runtime errors (NameError, TypeError, etc.)
            - logic: Logic errors (IndexError, KeyError, etc.)
            - import: Import/module errors
            - io: File I/O errors
            - network: Network/connection errors
        """
        syntax_errors = ["SyntaxError", "IndentationError", "TabError"]
        runtime_errors = ["NameError", "TypeError", "ValueError", "AttributeError"]
        logic_errors = ["IndexError", "KeyError", "ZeroDivisionError", "AssertionError"]
        import_errors = ["ImportError", "ModuleNotFoundError"]
        io_errors = ["FileNotFoundError", "IOError", "PermissionError"]
        network_errors = ["ConnectionError", "TimeoutError"]

        if error_type in syntax_errors:
            return "syntax"
        elif error_type in runtime_errors:
            return "runtime"
        elif error_type in logic_errors:
            return "logic"
        elif error_type in import_errors:
            return "import"
        elif error_type in io_errors:
            return "io"
        elif error_type in network_errors:
            return "network"
        else:
            return "unknown"
