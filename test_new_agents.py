"""
Test script for newly implemented LearnFlow agents

Tests the 3 new agents: Code Review, Debug, and Exercise Generator
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def test_imports():
    """Test that all modules can be imported"""
    print("=" * 60)
    print("TESTING IMPORTS")
    print("=" * 60)

    tests = [
        # Code Review Agent
        ("Code Review Config", "from backend.agents.code_review.config import config"),
        ("Code Review Models", "from backend.agents.code_review.models import CodeReviewRequest, CodeReviewResponse"),
        ("Code Review Routes", "from backend.agents.code_review.routes import router"),
        ("Code Review Services", "from backend.agents.code_review.services.reviewer import CodeReviewer"),

        # Debug Agent
        ("Debug Config", "from backend.agents.debug.config import config"),
        ("Debug Models", "from backend.agents.debug.models import DiagnosisRequest, DiagnosisResponse"),
        ("Debug Routes", "from backend.agents.debug.routes import router"),
        ("Debug Services", "from backend.agents.debug.services.debugger import Debugger"),
        ("Error Parser", "from backend.agents.debug.services.error_parser import ErrorParser"),

        # Exercise Generator
        ("Exercise Config", "from backend.agents.exercise.config import config"),
        ("Exercise Models", "from backend.agents.exercise.models import ExerciseGenerationRequest, Exercise"),
        ("Exercise Routes", "from backend.agents.exercise.routes import router"),
        ("Exercise Services", "from backend.agents.exercise.services.generator import ExerciseGenerator"),
        ("Difficulty Scaler", "from backend.agents.exercise.services.difficulty_scaler import DifficultyScaler"),
    ]

    passed = 0
    failed = 0

    for name, import_stmt in tests:
        try:
            exec(import_stmt)
            print(f"[PASS] {name}")
            passed += 1
        except Exception as e:
            print(f"[FAIL] {name}: {e}")
            failed += 1

    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0


def test_configurations():
    """Test agent configurations"""
    print("\n" + "=" * 60)
    print("TESTING CONFIGURATIONS")
    print("=" * 60)

    from backend.agents.code_review.config import config as code_review_config
    from backend.agents.debug.config import config as debug_config
    from backend.agents.exercise.config import config as exercise_config

    configs = [
        ("Code Review", code_review_config, 8003),
        ("Debug", debug_config, 8004),
        ("Exercise", exercise_config, 8005),
    ]

    passed = 0
    failed = 0

    for name, config, expected_port in configs:
        try:
            assert config.agent_port == expected_port, f"Expected port {expected_port}, got {config.agent_port}"
            print(f"[PASS] {name} Agent: {config.agent_name} on port {config.agent_port}")
            passed += 1
        except Exception as e:
            print(f"[FAIL] {name} Agent: {e}")
            failed += 1

    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0


def test_models():
    """Test Pydantic model instantiation"""
    print("\n" + "=" * 60)
    print("TESTING PYDANTIC MODELS")
    print("=" * 60)

    tests = []

    # Code Review
    try:
        from backend.agents.code_review.models import CodeReviewRequest
        req = CodeReviewRequest(
            query_id="test-001",
            student_id="s1",
            code="print('hello')",
            language="python"
        )
        print(f"[PASS] CodeReviewRequest: {req.query_id}")
        tests.append(True)
    except Exception as e:
        print(f"[FAIL] CodeReviewRequest: {e}")
        tests.append(False)

    # Debug
    try:
        from backend.agents.debug.models import DiagnosisRequest
        req = DiagnosisRequest(
            query_id="test-002",
            student_id="s1",
            error_message="NameError: name 'x' is not defined",
            language="python"
        )
        print(f"[PASS] DiagnosisRequest: {req.query_id}")
        tests.append(True)
    except Exception as e:
        print(f"[FAIL] DiagnosisRequest: {e}")
        tests.append(False)

    # Exercise
    try:
        from backend.agents.exercise.models import ExerciseGenerationRequest
        req = ExerciseGenerationRequest(
            query_id="test-003",
            student_id="s1",
            topic="loops",
            difficulty_level="beginner",
            count=3
        )
        print(f"[PASS] ExerciseGenerationRequest: {req.query_id}")
        tests.append(True)
    except Exception as e:
        print(f"[FAIL] ExerciseGenerationRequest: {e}")
        tests.append(False)

    passed = sum(tests)
    failed = len(tests) - passed
    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0


def test_error_parser():
    """Test error parser functionality"""
    print("\n" + "=" * 60)
    print("TESTING ERROR PARSER")
    print("=" * 60)

    try:
        from backend.agents.debug.services.error_parser import ErrorParser

        parser = ErrorParser()

        # Test error type extraction
        error_msg = "NameError: name 'x' is not defined"
        error_type = parser._extract_error_type(error_msg, "python")
        assert error_type == "NameError", f"Expected 'NameError', got '{error_type}'"
        print(f"[PASS] Error type extraction: {error_type}")

        # Test error classification
        category = parser.classify_error_category("NameError")
        assert category == "runtime", f"Expected 'runtime', got '{category}'"
        print(f"[PASS] Error classification: NameError -> {category}")

        # Test stack trace parsing
        stack_trace = """Traceback (most recent call last):
  File "test.py", line 10, in <module>
    print(x)
NameError: name 'x' is not defined"""

        parsed = parser.parse_error(error_msg, stack_trace, "python")
        assert parsed["error_type"] == "NameError"
        assert len(parsed["line_numbers"]) > 0
        print(f"[PASS] Stack trace parsing: {len(parsed['line_numbers'])} lines found")

        print("\nResults: 3 passed, 0 failed")
        return True

    except Exception as e:
        print(f"[FAIL] Error parser test failed: {e}")
        print("\nResults: 0 passed, 1 failed")
        return False


def test_difficulty_scaler():
    """Test difficulty scaler functionality"""
    print("\n" + "=" * 60)
    print("TESTING DIFFICULTY SCALER")
    print("=" * 60)

    try:
        from backend.agents.exercise.services.difficulty_scaler import DifficultyScaler

        scaler = DifficultyScaler()

        # Test difficulty recommendation
        tests = [
            (0.2, "beginner"),
            (0.5, "intermediate"),
            (0.7, "advanced"),
            (0.9, "expert")
        ]

        passed = 0
        for mastery, expected in tests:
            difficulty = scaler.recommend_difficulty(mastery_score=mastery)
            if difficulty == expected:
                print(f"[PASS] Mastery {mastery} -> {difficulty}")
                passed += 1
            else:
                print(f"[FAIL] Mastery {mastery} -> {difficulty} (expected {expected})")

        # Test exercise parameters
        params = scaler.get_exercise_parameters("beginner", "loops")
        assert params["complexity"] == "simple"
        print(f"[PASS] Exercise parameters: {params['complexity']}")
        passed += 1

        # Test next topic suggestions
        suggestions = scaler.suggest_next_topics("loops", 0.8)
        assert len(suggestions) > 0
        print(f"[PASS] Next topic suggestions: {', '.join(suggestions[:2])}")
        passed += 1

        print(f"\nResults: {passed} passed, 0 failed")
        return True

    except Exception as e:
        print(f"[FAIL] Difficulty scaler test failed: {e}")
        import traceback
        traceback.print_exc()
        print("\nResults: 0 passed, 1 failed")
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("LEARNFLOW AGENTS TEST SUITE")
    print("Testing: Code Review, Debug, Exercise Generator")
    print("=" * 60)

    results = []

    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Configurations", test_configurations()))
    results.append(("Pydantic Models", test_models()))
    results.append(("Error Parser", test_error_parser()))
    results.append(("Difficulty Scaler", test_difficulty_scaler()))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    for name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status}: {name}")

    total_passed = sum(1 for _, passed in results if passed)
    total_tests = len(results)

    print(f"\nOverall: {total_passed}/{total_tests} test suites passed")

    if total_passed == total_tests:
        print("\n==> All tests passed! Agents are ready for deployment.")
        return 0
    else:
        print("\n==> Some tests failed. Please review errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
