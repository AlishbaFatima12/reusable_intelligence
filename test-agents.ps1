# Test Script for LearnFlow Agents
# Run this after starting all 3 agents

Write-Host "🧪 Testing LearnFlow Backend Agents" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Health Checks
Write-Host "Test 1: Health Checks" -ForegroundColor Yellow
Write-Host "---------------------" -ForegroundColor Yellow

$agents = @(
    @{Name="Triage"; Port=8001},
    @{Name="Concepts"; Port=8002},
    @{Name="Progress"; Port=8006}
)

foreach ($agent in $agents) {
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:$($agent.Port)/health" -Method Get
        if ($response.status -eq "healthy") {
            Write-Host "✅ $($agent.Name) Agent (port $($agent.Port)): HEALTHY" -ForegroundColor Green
        } else {
            Write-Host "❌ $($agent.Name) Agent: Unhealthy" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ $($agent.Name) Agent: NOT RUNNING (Is it started?)" -ForegroundColor Red
    }
}

Write-Host ""

# Test 2: Triage Agent - Query Classification
Write-Host "Test 2: Triage Agent - Query Classification" -ForegroundColor Yellow
Write-Host "-------------------------------------------" -ForegroundColor Yellow

try {
    $body = @{
        query_id = "test-001"
        student_id = "student-123"
        query_text = "What is recursion in Python?"
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:8001/api/v1/analyze" -Method Post -Body $body -ContentType "application/json"

    Write-Host "✅ Query classified successfully!" -ForegroundColor Green
    Write-Host "   Intent: $($response.detected_intent)" -ForegroundColor Cyan
    Write-Host "   Confidence: $($response.confidence_score)" -ForegroundColor Cyan
    Write-Host "   Routed to: $($response.routed_to_agent)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Triage classification failed: $_" -ForegroundColor Red
}

Write-Host ""

# Test 3: Concepts Agent - Generate Explanation
Write-Host "Test 3: Concepts Agent - Generate Explanation" -ForegroundColor Yellow
Write-Host "---------------------------------------------" -ForegroundColor Yellow

try {
    $body = @{
        query_id = "test-002"
        student_id = "student-123"
        concept = "variables"
        difficulty_level = "beginner"
        include_examples = $true
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:8002/api/v1/explain" -Method Post -Body $body -ContentType "application/json"

    Write-Host "✅ Explanation generated successfully!" -ForegroundColor Green
    Write-Host "   Concept: $($response.concept)" -ForegroundColor Cyan
    Write-Host "   Examples provided: $($response.code_examples.Count)" -ForegroundColor Cyan
    Write-Host "   Processing time: $($response.processing_time_ms)ms" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Concept explanation failed: $_" -ForegroundColor Red
    Write-Host "   (This uses Claude API - check your API key in .env)" -ForegroundColor Yellow
}

Write-Host ""

# Test 4: Progress Tracker - Get Mastery
Write-Host "Test 4: Progress Tracker - Get Mastery" -ForegroundColor Yellow
Write-Host "--------------------------------------" -ForegroundColor Yellow

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8006/api/v1/mastery/student-123" -Method Get

    Write-Host "✅ Mastery data retrieved!" -ForegroundColor Green
    Write-Host "   Student: $($response.student_id)" -ForegroundColor Cyan
    Write-Host "   Overall Mastery: $([math]::Round($response.overall_mastery * 100, 1))%" -ForegroundColor Cyan
    Write-Host "   Topics tracked: $($response.topic_mastery.Count)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Progress Tracker failed: $_" -ForegroundColor Red
}

Write-Host ""

# Test 5: Update Mastery
Write-Host "Test 5: Progress Tracker - Update Mastery" -ForegroundColor Yellow
Write-Host "-----------------------------------------" -ForegroundColor Yellow

try {
    $body = @{
        student_id = "student-123"
        topic = "functions"
        interaction_type = "success"
        success = $true
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:8006/api/v1/mastery/student-123" -Method Post -Body $body -ContentType "application/json"

    Write-Host "✅ Mastery updated successfully!" -ForegroundColor Green
    Write-Host "   New Overall Mastery: $([math]::Round($response.overall_mastery * 100, 1))%" -ForegroundColor Cyan
    Write-Host "   Next recommended topic: $($response.next_recommended_topic)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Mastery update failed: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "✅ Testing Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Check agent terminal windows for logs" -ForegroundColor White
Write-Host "2. Open frontend: cd mystery-skils-app-ui && npm run dev" -ForegroundColor White
Write-Host "3. Visit http://localhost:4000 to see the UI" -ForegroundColor White
