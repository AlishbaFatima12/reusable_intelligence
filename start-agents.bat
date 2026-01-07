@echo off
echo ========================================
echo LearnFlow - Start All Backend Agents
echo ========================================
echo.
echo This will open 3 terminal windows:
echo   1. Triage Agent (Port 8001)
echo   2. Concepts Agent (Port 8002)
echo   3. Progress Tracker (Port 8006)
echo.
echo Make sure you have:
echo   - Created venv: python -m venv venv
echo   - Installed deps: pip install -r backend/requirements.txt
echo   - Set API key in .env file
echo.
pause

echo.
echo Starting agents...
echo.

REM Start Triage Agent
start "Triage Agent (8001)" cmd /k "cd /d %~dp0 && venv\Scripts\activate && cd backend\agents\triage && uvicorn main:app --host 0.0.0.0 --port 8001 --reload"

REM Wait 2 seconds
timeout /t 2 /nobreak >nul

REM Start Concepts Agent
start "Concepts Agent (8002)" cmd /k "cd /d %~dp0 && venv\Scripts\activate && cd backend\agents\concepts && uvicorn main:app --host 0.0.0.0 --port 8002 --reload"

REM Wait 2 seconds
timeout /t 2 /nobreak >nul

REM Start Progress Tracker
start "Progress Tracker (8006)" cmd /k "cd /d %~dp0 && venv\Scripts\activate && cd backend\agents\progress && uvicorn main:app --host 0.0.0.0 --port 8006 --reload"

echo.
echo ✓ All agents starting...
echo.
echo Check the 3 new terminal windows for agent logs.
echo Wait ~5 seconds for all agents to fully start.
echo.
echo To test: Run test-agents.ps1 in PowerShell
echo To stop: Close each terminal window (or press Ctrl+C in each)
echo.
pause
