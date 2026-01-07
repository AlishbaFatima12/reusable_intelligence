"""
Complete LearnFlow System Test

Tests all 6 agents with real requests and verifies responses.
"""

import requests
import json
import time
from datetime import datetime


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'


def print_test(name, status, message=""):
    """Print formatted test result"""
    symbol = "✓" if status else "✗"
    color = Colors.GREEN if status else Colors.RED
    print(f"{color}[{symbol}] {name}{Colors.RESET}", end="")
    if message:
        print(f" - {message}")
    else:
        print()


def test_agent_health(name, port):
    """Test agent health endpoint"""
    try:
        response = requests.get(f"http://localhost:{port}/health", timeout=5)
        data = response.json()
        print_test(f"{name} Agent Health", response.status_code == 200,
                   f"Status: {data.get('status', 'unknown')}")
        return response.status_code == 200
    except Exception as e:
        print_test(f"{name} Agent Health", False, f"Error: {str(e)}")
        return False


def test_triage_agent():
    """Test Triage Agent query analysis"""
    print(f"\n{Colors.BLUE}Testing Triage Agent...{Colors.RESET}")

    try:
        response = requests.post(
            "http://localhost:8001/api/v1/analyze",
            json={
                "query_id": "test-triage-001",
                "student_id": "test-student",
                "query_text": "What is a variable in Python?",
                "code_snippet": None
            },
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            print_test("Query Analysis", True,
                       f"Intent: {data.get('detected_intent')}, "
                       f"Confidence: {data.get('confidence_score', 0):.2f}")
            return True
        else:
            print_test("Query Analysis", False, f"Status: {response.status_code}")
            return False

    except Exception as e:
        print_test("Query Analysis", False, f"Error: {str(e)}")
        return False


def test_concepts_agent():
    """Test Concepts Agent explanation"""
    print(f"\n{Colors.BLUE}Testing Concepts Agent...{Colors.RESET}")

    try:
        response = requests.post(
            "http://localhost:8002/api/v1/explain",
            json={
                "query_id": "test-concepts-001",
                "student_id": "test-student",
                "concept": "list comprehension",
                "difficulty_level": "beginner"
            },
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()
            print_test("Concept Explanation", True,
                       f"Has explanation: {bool(data.get('explanation'))}, "
                       f"Examples: {len(data.get('code_examples', []))}")
            return True
        else:
            print_test("Concept Explanation", False, f"Status: {response.status_code}")
            return False

    except Exception as e:
        print_test("Concept Explanation", False, f"Error: {str(e)}")
        return False


def test_code_review_agent():
    """Test Code Review Agent"""
    print(f"\n{Colors.BLUE}Testing Code Review Agent...{Colors.RESET}")

    try:
        response = requests.post(
            "http://localhost:8003/api/v1/review",
            json={
                "query_id": "test-review-001",
                "student_id": "test-student",
                "code": "def calculate_sum(numbers):\n    total = 0\n    for num in numbers:\n        total = total + num\n    return total",
                "language": "python",
                "context": "Calculate sum of a list of numbers"
            },
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()
            print_test("Code Review", True,
                       f"Rating: {data.get('overall_rating')}, "
                       f"Feedback items: {len(data.get('feedback_items', []))}")
            return True
        else:
            print_test("Code Review", False, f"Status: {response.status_code}")
            return False

    except Exception as e:
        print_test("Code Review", False, f"Error: {str(e)}")
        return False


def test_debug_agent():
    """Test Debug Agent"""
    print(f"\n{Colors.BLUE}Testing Debug Agent...{Colors.RESET}")

    try:
        response = requests.post(
            "http://localhost:8004/api/v1/diagnose",
            json={
                "query_id": "test-debug-001",
                "student_id": "test-student",
                "error_message": "NameError: name 'total' is not defined",
                "code_snippet": "def sum_numbers(nums):\n    for n in nums:\n        total += n\n    return total",
                "error_type": "runtime"
            },
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()
            print_test("Error Diagnosis", True,
                       f"Error type: {data.get('error_classification')}, "
                       f"Has root cause: {bool(data.get('root_cause_analysis'))}")
            return True
        else:
            print_test("Error Diagnosis", False, f"Status: {response.status_code}")
            return False

    except Exception as e:
        print_test("Error Diagnosis", False, f"Error: {str(e)}")
        return False


def test_exercise_agent():
    """Test Exercise Generator Agent"""
    print(f"\n{Colors.BLUE}Testing Exercise Generator...{Colors.RESET}")

    try:
        response = requests.post(
            "http://localhost:8005/api/v1/generate",
            json={
                "query_id": "test-exercise-001",
                "student_id": "test-student",
                "topic": "loops",
                "difficulty": "beginner",
                "count": 2
            },
            timeout=20
        )

        if response.status_code == 200:
            data = response.json()
            exercises = data.get('exercises', [])
            print_test("Exercise Generation", True,
                       f"Generated: {len(exercises)} exercises")

            if exercises:
                ex = exercises[0]
                print(f"  First exercise: {ex.get('title', 'No title')}")

            return True
        else:
            print_test("Exercise Generation", False, f"Status: {response.status_code}")
            return False

    except Exception as e:
        print_test("Exercise Generation", False, f"Error: {str(e)}")
        return False


def test_progress_agent():
    """Test Progress Tracker Agent"""
    print(f"\n{Colors.BLUE}Testing Progress Tracker...{Colors.RESET}")

    student_id = "test-student-complete"

    # Create some progress data
    topics = [
        ("variables-and-data-types", 8, 2),
        ("control-flow", 6, 4),
        ("data-structures", 3, 7),
    ]

    try:
        for topic, successes, failures in topics:
            for _ in range(successes):
                requests.post(
                    f"http://localhost:8006/api/v1/mastery/{student_id}",
                    json={
                        "student_id": student_id,
                        "topic": topic,
                        "interaction_type": "success",
                        "success": True
                    },
                    timeout=5
                )

            for _ in range(failures):
                requests.post(
                    f"http://localhost:8006/api/v1/mastery/{student_id}",
                    json={
                        "student_id": student_id,
                        "topic": topic,
                        "interaction_type": "error",
                        "success": False
                    },
                    timeout=5
                )

        # Get mastery data
        response = requests.get(
            f"http://localhost:8006/api/v1/mastery/{student_id}",
            timeout=5
        )

        if response.status_code == 200:
            data = response.json()
            overall = data.get('overall_mastery', 0) * 100
            topics_count = len(data.get('topic_mastery', []))

            print_test("Progress Tracking", True,
                       f"Overall: {overall:.1f}%, Topics: {topics_count}")

            # Show topic breakdown
            for topic in data.get('topic_mastery', []):
                mastery = topic['mastery_percentage']
                color = Colors.GREEN if mastery >= 70 else Colors.YELLOW if mastery >= 40 else Colors.RED
                print(f"  {color}{topic['topic_name']}: {mastery:.1f}%{Colors.RESET}")

            return True
        else:
            print_test("Progress Tracking", False, f"Status: {response.status_code}")
            return False

    except Exception as e:
        print_test("Progress Tracking", False, f"Error: {str(e)}")
        return False


def main():
    """Run all tests"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}LearnFlow Complete System Test{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}\n")

    start_time = time.time()

    # Test health endpoints
    print(f"{Colors.YELLOW}Phase 1: Agent Health Checks{Colors.RESET}")
    agents = [
        ("Triage", 8001),
        ("Concepts", 8002),
        ("Code Review", 8003),
        ("Debug", 8004),
        ("Exercise", 8005),
        ("Progress", 8006),
    ]

    health_results = []
    for name, port in agents:
        health_results.append(test_agent_health(name, port))

    # Test functionality
    print(f"\n{Colors.YELLOW}Phase 2: Functional Tests{Colors.RESET}")
    functional_tests = [
        test_triage_agent,
        test_concepts_agent,
        test_code_review_agent,
        test_debug_agent,
        test_exercise_agent,
        test_progress_agent,
    ]

    functional_results = []
    for test_func in functional_tests:
        functional_results.append(test_func())
        time.sleep(1)  # Small delay between tests

    # Summary
    elapsed = time.time() - start_time
    total_tests = len(health_results) + len(functional_results)
    passed_tests = sum(health_results) + sum(functional_results)

    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.YELLOW}Test Summary{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}\n")

    success_rate = (passed_tests / total_tests) * 100
    color = Colors.GREEN if success_rate >= 90 else Colors.YELLOW if success_rate >= 70 else Colors.RED

    print(f"Total Tests: {total_tests}")
    print(f"Passed: {color}{passed_tests}{Colors.RESET}")
    print(f"Failed: {Colors.RED}{total_tests - passed_tests}{Colors.RESET}")
    print(f"Success Rate: {color}{success_rate:.1f}%{Colors.RESET}")
    print(f"Time Elapsed: {elapsed:.2f}s\n")

    if success_rate == 100:
        print(f"{Colors.GREEN}🎉 All tests passed! System is fully operational.{Colors.RESET}\n")
    elif success_rate >= 50:
        print(f"{Colors.YELLOW}⚠️  Some tests failed. Check agent logs for details.{Colors.RESET}\n")
    else:
        print(f"{Colors.RED}❌ Most tests failed. Please check if all agents are running.{Colors.RESET}\n")

    print(f"{Colors.BLUE}Next Steps:{Colors.RESET}")
    print("1. Check http://localhost:4000/mystery-skills-flash.html")
    print("2. Verify mastery data displays in dashboard")
    print("3. Test individual endpoints with curl\n")


if __name__ == "__main__":
    main()
