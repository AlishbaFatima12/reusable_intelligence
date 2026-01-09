@echo off
echo Killing all backend agents...
echo.

for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8001" ^| findstr "LISTENING"') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8002" ^| findstr "LISTENING"') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8003" ^| findstr "LISTENING"') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8004" ^| findstr "LISTENING"') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8005" ^| findstr "LISTENING"') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8006" ^| findstr "LISTENING"') do taskkill /F /PID %%a 2>nul

echo.
echo All agents stopped!
echo.
echo Now run: start-agents.bat
pause
