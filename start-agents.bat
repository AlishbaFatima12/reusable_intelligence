@echo off
echo ========================================
echo LearnFlow - Start All Backend Agents
echo ========================================
echo.
echo This will open 6 terminal windows:
echo   1. Triage Agent (Port 8001)
echo   2. Concepts Agent (Port 8002)
echo   3. Code Review Agent (Port 8003)
echo   4. Debug Agent (Port 8004)
echo   5. Exercise Generator (Port 8005)
echo   6. Progress Tracker (Port 8006)
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

REM Set environment variables for all agents
REM NOTE: Set your ANTHROPIC_API_KEY in system environment variables or .env file
REM set ANTHROPIC_API_KEY=your-api-key-here
set CLAUDE_MODEL=claude-sonnet-3-5-20241022

REM Start Triage Agent
start "Triage Agent (8001)" cmd /k "cd /d %~dp0 && set PYTHONPATH=%~dp0 && set ANTHROPIC_API_KEY=%ANTHROPIC_API_KEY% && set CLAUDE_MODEL=%CLAUDE_MODEL% && venv\Scripts\activate && venv\Scripts\python -m uvicorn backend.agents.triage.main:app --host 0.0.0.0 --port 8001 --reload"

REM Wait 2 seconds
timeout /t 2 /nobreak >nul

REM Start Concepts Agent
start "Concepts Agent (8002)" cmd /k "cd /d %~dp0 && set PYTHONPATH=%~dp0 && set ANTHROPIC_API_KEY=%ANTHROPIC_API_KEY% && set CLAUDE_MODEL=%CLAUDE_MODEL% && venv\Scripts\activate && venv\Scripts\python -m uvicorn backend.agents.concepts.main:app --host 0.0.0.0 --port 8002 --reload"

REM Wait 2 seconds
timeout /t 2 /nobreak >nul

REM Start Code Review Agent
start "Code Review Agent (8003)" cmd /k "cd /d %~dp0 && set PYTHONPATH=%~dp0 && set ANTHROPIC_API_KEY=%ANTHROPIC_API_KEY% && set CLAUDE_MODEL=%CLAUDE_MODEL% && venv\Scripts\activate && venv\Scripts\python -m uvicorn backend.agents.code_review.main:app --host 0.0.0.0 --port 8003 --reload"

REM Wait 2 seconds
timeout /t 2 /nobreak >nul

REM Start Debug Agent
start "Debug Agent (8004)" cmd /k "cd /d %~dp0 && set PYTHONPATH=%~dp0 && set ANTHROPIC_API_KEY=%ANTHROPIC_API_KEY% && set CLAUDE_MODEL=%CLAUDE_MODEL% && venv\Scripts\activate && venv\Scripts\python -m uvicorn backend.agents.debug.main:app --host 0.0.0.0 --port 8004 --reload"

REM Wait 2 seconds
timeout /t 2 /nobreak >nul

REM Start Exercise Generator
start "Exercise Generator (8005)" cmd /k "cd /d %~dp0 && set PYTHONPATH=%~dp0 && set ANTHROPIC_API_KEY=%ANTHROPIC_API_KEY% && set CLAUDE_MODEL=%CLAUDE_MODEL% && venv\Scripts\activate && venv\Scripts\python -m uvicorn backend.agents.exercise.main:app --host 0.0.0.0 --port 8005 --reload"

REM Wait 2 seconds
timeout /t 2 /nobreak >nul

REM Start Progress Tracker
start "Progress Tracker (8006)" cmd /k "cd /d %~dp0 && set PYTHONPATH=%~dp0 && set ANTHROPIC_API_KEY=%ANTHROPIC_API_KEY% && set CLAUDE_MODEL=%CLAUDE_MODEL% && venv\Scripts\activate && venv\Scripts\python -m uvicorn backend.agents.progress.main:app --host 0.0.0.0 --port 8006 --reload"

echo.
echo ✓ All agents starting...
echo.
echo Check the 6 new terminal windows for agent logs.
echo Wait ~15 seconds for all agents to fully start.
echo.
echo To test: Run test-agents.ps1 in PowerShell
echo To stop: Close each terminal window (or press Ctrl+C in each)
echo.
pause
