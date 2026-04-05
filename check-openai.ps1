#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Script simples para verificar OpenAI API Key
#>

Write-Host "`n╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  Diagnóstico: OpenAI API Configuration             ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

$envFile = "C:\Projects\Saas\.env"

# Verificar .env
Write-Host "1. Verificando arquivo .env..." -ForegroundColor Yellow
if (Test-Path $envFile) {
    Write-Host "   OK: Arquivo encontrado" -ForegroundColor Green

    $lines = Get-Content $envFile
    $apiKeyLine = $lines | Where-Object { $_ -like "OPENAI_API_KEY=*" }

    if ($apiKeyLine) {
        $keyValue = $apiKeyLine -replace "OPENAI_API_KEY=", ""

        if ($keyValue -eq "your-openai-api-key-here" -or $keyValue -eq "") {
            Write-Host "   ERRO: Chave é placeholder ou vazia" -ForegroundColor Red
            Write-Host "   Sistema em MODO MOCK" -ForegroundColor Red
        } elseif ($keyValue -like "sk-proj-*") {
            Write-Host "   OK: Chave OpenAI válida detectada!" -ForegroundColor Green
            $prefix = $keyValue.Substring(0, [Math]::Min(15, $keyValue.Length))
            Write-Host "   Começa com: $prefix..." -ForegroundColor Cyan
        } else {
            Write-Host "   AVISO: Formato inválido. Esperado: sk-proj-..." -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "   ERRO: Arquivo não encontrado" -ForegroundColor Red
}

# Verificar Docker
Write-Host "`n2. Verificando Docker..." -ForegroundColor Yellow
$dockerCheck = docker ps 2>&1 | Select-String "resume-optimizer"
if ($dockerCheck) {
    Write-Host "   OK: Containers encontrados" -ForegroundColor Green
} else {
    Write-Host "   AVISO: Nenhum container rodando" -ForegroundColor Yellow
}

# Status final
Write-Host "`n════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host "`nSTATUS FINAL:" -ForegroundColor Cyan

$content = Get-Content $envFile -Raw
$isValid = $false
if ($content -match "OPENAI_API_KEY=(.+?)(?=`r?`n|`n|$)") {
    $key = $matches[1].Trim()
    if ($key -like "sk-proj-*" -and $key.Length -gt 20) {
        $isValid = $true
    }
}

if ($isValid) {
    Write-Host "✅ Sistema CONFIGURADO com OpenAI valido" -ForegroundColor Green
    Write-Host "   - ATS Score vai usar analise IA real" -ForegroundColor Green
    Write-Host "   - Optimized Resume vai gerar otimizacoes" -ForegroundColor Green
} else {
    Write-Host "❌ Sistema em MODO MOCK (sem chave OpenAI valida)" -ForegroundColor Red
    Write-Host "`n🔧 Para configurar:" -ForegroundColor Yellow
    Write-Host "   1. Obtenha em: https://platform.openai.com/api-keys" -ForegroundColor Cyan
    Write-Host "   2. Edite C:\Projects\Saas\.env" -ForegroundColor Cyan
    Write-Host "   3. Mude OPENAI_API_KEY=your-openai-api-key-here" -ForegroundColor Cyan
    Write-Host "   4. Para OPENAI_API_KEY=sk-proj-SUA-CHAVE-AQUI" -ForegroundColor Green
    Write-Host "   5. Reinicie: cd docker && docker-compose restart" -ForegroundColor Cyan
}

Write-Host "`n════════════════════════════════════════════════════════`n" -ForegroundColor Gray



