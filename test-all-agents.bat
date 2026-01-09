@echo off
echo ========================================
echo Testing All LearnFlow Agents
echo ========================================
echo.

echo [1/6] Testing Triage Agent (Port 8001)...
curl -s http://localhost:8001/health
echo.

echo [2/6] Testing Concepts Agent (Port 8002)...
curl -s http://localhost:8002/health
echo.

echo [3/6] Testing Code Review Agent (Port 8003)...
curl -s http://localhost:8003/health
echo.

echo [4/6] Testing Debug Agent (Port 8004)...
curl -s http://localhost:8004/health
echo.

echo [5/6] Testing Exercise Agent (Port 8005)...
curl -s http://localhost:8005/health
echo.

echo [6/6] Testing Progress Agent (Port 8006)...
curl -s http://localhost:8006/health
echo.

echo ========================================
echo All agents tested!
echo ========================================
echo.

echo Testing Progress Agent data...
curl -s http://localhost:8006/api/v1/mastery/demo-student-001
echo.

pause
