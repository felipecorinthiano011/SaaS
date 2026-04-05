$ErrorActionPreference = "Stop"

Write-Host "=== Testing login ==="
$loginBody = '{"email":"demo@test.com","password":"demo1234"}'
$loginResp = Invoke-RestMethod -Method Post -Uri "http://localhost:8080/api/auth/login" -Body $loginBody -ContentType "application/json"
Write-Host "Login OK. Token: $($loginResp.token.Substring(0,30))..."

$headers = @{ Authorization = "Bearer $($loginResp.token)" }

Write-Host ""
Write-Host "=== Testing register new user ==="
try {
    $regBody = '{"email":"testuser2@example.com","password":"password123"}'
    $regResp = Invoke-RestMethod -Method Post -Uri "http://localhost:8080/api/auth/register" -Body $regBody -ContentType "application/json"
    Write-Host "Register OK. Token: $($regResp.token.Substring(0,30))..."
} catch {
    Write-Host "Register skipped (user may already exist)"
}

Write-Host ""
Write-Host "=== Testing analyze ==="
$analyzeBody = '{"jobDescription":"Senior Java developer with Spring Boot and PostgreSQL experience. Docker and Kubernetes required. Agile scrum methodology.","resumeText":"Software engineer with 6 years Java Spring Boot experience. Docker containers and PostgreSQL databases. Agile development."}'
$result = Invoke-RestMethod -Method Post -Uri "http://localhost:8080/api/job/analyze" -Body $analyzeBody -ContentType "application/json" -Headers $headers
Write-Host "Analyze OK!"
Write-Host "  ID:           $($result.id)"
Write-Host "  ATS Score:    $($result.atsScore)"
Write-Host "  Extracted:    $($result.extractedKeywords -join ', ')"
Write-Host "  Missing:      $($result.missingKeywords -join ', ')"
Write-Host "  Suggestions:  $($result.suggestions.Count)"
Write-Host "  Gap Summary:  $($result.gapSummary)"

Write-Host ""
Write-Host "=== Testing list analyses ==="
$list = Invoke-RestMethod -Method Get -Uri "http://localhost:8080/api/job" -Headers $headers
Write-Host "List OK! Count: $($list.Count)"
if ($list.Count -gt 0) {
    Write-Host "  Latest ATS: $($list[0].atsScore)  ID: $($list[0].id)"
}

Write-Host ""
Write-Host "=== All tests passed! ==="

