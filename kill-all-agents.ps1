# PowerShell script to forcefully kill all backend agents

Write-Host "Killing all backend agent processes..." -ForegroundColor Yellow

# Find and kill processes on each agent port
$ports = @(8001, 8002, 8003, 8004, 8005, 8006)

foreach ($port in $ports) {
    $connections = netstat -ano | Select-String ":$port " | Select-String "LISTENING"

    foreach ($conn in $connections) {
        $parts = $conn -split '\s+'
        $pid = $parts[-1]

        if ($pid -match '^\d+$') {
            Write-Host "Killing process $pid on port $port..." -ForegroundColor Red
            try {
                Stop-Process -Id $pid -Force -ErrorAction Stop
                Write-Host "  ✓ Killed PID $pid" -ForegroundColor Green
            } catch {
                Write-Host "  ✗ Failed to kill PID $pid" -ForegroundColor DarkRed
            }
        }
    }
}

Write-Host ""
Write-Host "All agents stopped!" -ForegroundColor Green
Write-Host "Now run: start-agents.bat" -ForegroundColor Cyan
