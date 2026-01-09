# Pre-flight Check Script for LearnFlow Platform
# Run this before starting agents to verify environment

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "LearnFlow Platform - Pre-flight Check" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# Check 1: Virtual Environment
Write-Host "[1/5] Checking virtual environment..." -NoNewline
if (Test-Path "venv\Scripts\python.exe") {
    Write-Host " OK" -ForegroundColor Green
    $pythonVersion = & venv\Scripts\python.exe --version
    Write-Host "      $pythonVersion" -ForegroundColor Gray
} else {
    Write-Host " FAILED" -ForegroundColor Red
    Write-Host "      Virtual environment not found!" -ForegroundColor Red
    Write-Host "      Run: python -m venv venv" -ForegroundColor Yellow
    $allGood = $false
}

# Check 2: Required Packages
Write-Host "[2/5] Checking required packages..." -NoNewline
try {
    & venv\Scripts\python.exe -c "import fastapi, uvicorn, anthropic, pydantic" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host " OK" -ForegroundColor Green
    } else {
        throw "Import failed"
    }
} catch {
    Write-Host " FAILED" -ForegroundColor Red
    Write-Host "      Required packages not installed!" -ForegroundColor Red
    Write-Host "      Run: venv\Scripts\pip install -r backend\requirements-minimal.txt" -ForegroundColor Yellow
    $allGood = $false
}

# Check 3: .env File and API Key
Write-Host "[3/5] Checking .env configuration..." -NoNewline
if (Test-Path ".env") {
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "ANTHROPIC_API_KEY=sk-ant-") {
        Write-Host " OK" -ForegroundColor Green
    } else {
        Write-Host " WARNING" -ForegroundColor Yellow
        Write-Host "      API key not set in .env file!" -ForegroundColor Yellow
        Write-Host "      Edit .env and add: ANTHROPIC_API_KEY=sk-ant-your-key" -ForegroundColor Yellow
        $allGood = $false
    }
} else {
    Write-Host " FAILED" -ForegroundColor Red
    Write-Host "      .env file not found!" -ForegroundColor Red
    Write-Host "      Copy .env.example to .env and add your API key" -ForegroundColor Yellow
    $allGood = $false
}

# Check 4: Agent Files
Write-Host "[4/5] Checking agent files..." -NoNewline
$agents = @("triage", "concepts", "progress")
$agentsMissing = @()
foreach ($agent in $agents) {
    if (-not (Test-Path "backend\agents\$agent\main.py")) {
        $agentsMissing += $agent
    }
}
if ($agentsMissing.Count -eq 0) {
    Write-Host " OK" -ForegroundColor Green
    Write-Host "      Found: Triage, Concepts, Progress" -ForegroundColor Gray
} else {
    Write-Host " FAILED" -ForegroundColor Red
    Write-Host "      Missing agents: $($agentsMissing -join ', ')" -ForegroundColor Red
    $allGood = $false
}

# Check 5: Port Availability
Write-Host "[5/5] Checking port availability..." -NoNewline
$ports = @(8001, 8002, 8006)
$portsInUse = @()
foreach ($port in $ports) {
    $connection = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    if ($connection) {
        $portsInUse += $port
    }
}
if ($portsInUse.Count -eq 0) {
    Write-Host " OK" -ForegroundColor Green
} else {
    Write-Host " WARNING" -ForegroundColor Yellow
    Write-Host "      Ports in use: $($portsInUse -join ', ')" -ForegroundColor Yellow
    Write-Host "      Stop existing processes or they will conflict" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

if ($allGood) {
    Write-Host "All checks passed! Ready to start agents." -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor White
    Write-Host "  1. Run: .\start-agents.bat" -ForegroundColor Yellow
    Write-Host "  2. Wait ~5 seconds for agents to start" -ForegroundColor Yellow
    Write-Host "  3. Run: .\test-agents.ps1" -ForegroundColor Yellow
    Write-Host "  4. Start frontend: cd mystery-skils-app-ui && npm run dev" -ForegroundColor Yellow
} else {
    Write-Host "Some checks failed. Fix issues above before starting." -ForegroundColor Red
}

Write-Host "========================================" -ForegroundColor Cyan
