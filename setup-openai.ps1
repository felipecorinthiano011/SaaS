#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Valida e configura a chave OpenAI para o SaaS Resume Optimizer

.DESCRIPTION
    - Verifica se .env existe
    - Verifica se OPENAI_API_KEY está configurada
    - Valida a chave OpenAI
    - Restart dos containers se necessário

.EXAMPLE
    .\setup-openai.ps1
    .\setup-openai.ps1 -ApiKey "sk-proj-xxxxx"
    .\setup-openai.ps1 -Validate
#>

param(
    [string]$ApiKey = "",
    [switch]$Validate = $false,
    [switch]$Reset = $false
)

$ErrorActionPreference = "Stop"
$PSDefaultParameterValues["*:Encoding"] = "UTF8"

$EnvFile = "C:\Projects\Saas\.env"
$DockerDir = "C:\Projects\Saas\docker"

Write-Host "`n╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   OpenAI Configuration for Resume Optimizer        ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# Função: Verificar se .env existe
function Test-EnvFile {
    if (-not (Test-Path $EnvFile)) {
        Write-Host "❌ Arquivo .env não encontrado!" -ForegroundColor Red
        Write-Host "   Local esperado: $EnvFile" -ForegroundColor Yellow
        return $false
    }
    Write-Host "✅ Arquivo .env encontrado" -ForegroundColor Green
    return $true
}

# Função: Ler .env
function Get-EnvValue {
    param([string]$Key)

    $content = Get-Content $EnvFile -Raw
    if ($content -match "^$Key=(.+?)(?=`r?`n|$)") {
        return $matches[1].Trim()
    }
    return ""
}

# Função: Atualizar .env
function Update-EnvValue {
    param(
        [string]$Key,
        [string]$Value
    )

    $content = Get-Content $EnvFile -Raw

    if ($content -match "^$Key=") {
        $content = $content -replace "^$Key=.+?(?=`r?`n|$)", "$Key=$Value"
    } else {
        $content += "`n$Key=$Value"
    }

    Set-Content -Path $EnvFile -Value $content -Encoding UTF8
    Write-Host "✅ Arquivo .env atualizado" -ForegroundColor Green
}

# Função: Validar formato da chave
function Test-ApiKeyFormat {
    param([string]$Key)

    if ($Key -match "^sk-proj-[a-zA-Z0-9_-]{20,}$") {
        return $true
    }
    return $false
}

# Função: Validar chave com OpenAI
function Test-ApiKey {
    param([string]$Key)

    if (-not (Test-ApiKeyFormat $Key)) {
        Write-Host "❌ Formato de chave inválido!" -ForegroundColor Red
        Write-Host "   Esperado: sk-proj-..." -ForegroundColor Yellow
        return $false
    }

    Write-Host "⏳ Testando chave com OpenAI..." -ForegroundColor Yellow

    try {
        $response = Invoke-WebRequest -Uri "https://api.openai.com/v1/models/gpt-4o-mini" `
            -Method GET `
            -Headers @{"Authorization" = "Bearer $Key"} `
            -TimeoutSec 5 -ErrorAction Stop

        if ($response.StatusCode -eq 200) {
            Write-Host "✅ Chave válida e ativa!" -ForegroundColor Green
            return $true
        }
    } catch {
        Write-Host "❌ Chave rejeitada pela OpenAI" -ForegroundColor Red
        Write-Host "   Erro: $($_.Exception.Message)" -ForegroundColor Yellow
        return $false
    }
}

# Função: Verificar Docker
function Test-Docker {
    try {
        $containers = docker ps --format "table {{.Names}}" 2>$null
        if ($containers -match "resume-optimizer") {
            Write-Host "✅ Docker containers estão rodando" -ForegroundColor Green
            return $true
        } else {
            Write-Host "⚠️  Docker containers não estão rodando" -ForegroundColor Yellow
            return $false
        }
    } catch {
        Write-Host "❌ Docker não está disponível" -ForegroundColor Red
        return $false
    }
}

# Função: Verificar chave nos containers
function Test-ContainerApiKey {
    try {
        Write-Host "⏳ Verificando chave no container AI..." -ForegroundColor Yellow

        $result = docker exec resume-optimizer-ai python -c "
from app.core.config import settings
if settings.openai_api_key:
    print(f'CONFIGURED:{settings.openai_api_key[:10]}')
else:
    print('NOT_SET')
" 2>$null

        if ($result -match "CONFIGURED:(.+)") {
            Write-Host "✅ Chave está configurada no container" -ForegroundColor Green
            Write-Host "   Primeiros 10 caracteres: $($matches[1])" -ForegroundColor Cyan
            return $true
        } else {
            Write-Host "❌ Chave não está configurada no container" -ForegroundColor Red
            return $false
        }
    } catch {
        Write-Host "⚠️  Erro ao verificar container (pode não estar rodando)" -ForegroundColor Yellow
        return $false
    }
}

# Função: Restart containers
function Restart-Containers {
    Write-Host "`n⏳ Reiniciando containers..." -ForegroundColor Yellow

    try {
        Push-Location $DockerDir
        docker-compose restart ai-service backend 2>&1 | Select-String -Pattern "Started|Restarted" | ForEach-Object { Write-Host $_ -ForegroundColor Green }

        Write-Host "⏳ Aguardando containers ficarem healthy (30 segundos)..." -ForegroundColor Yellow
        Start-Sleep -Seconds 30

        $health = docker-compose ps | Select-String -Pattern "healthy"
        if ($health.Count -ge 2) {
            Write-Host "✅ Containers reiniciados com sucesso!" -ForegroundColor Green
            return $true
        } else {
            Write-Host "⚠️  Containers podem não estar prontos ainda" -ForegroundColor Yellow
            return $false
        }
    } catch {
        Write-Host "❌ Erro ao reiniciar containers: $_" -ForegroundColor Red
        return $false
    } finally {
        Pop-Location
    }
}

# ===== MAIN FLOW =====

if (-not (Test-EnvFile)) {
    Write-Host "Configure o arquivo .env primeiro!" -ForegroundColor Red
    exit 1
}

$currentKey = Get-EnvValue "OPENAI_API_KEY"
Write-Host "Chave atual: $(if ($currentKey -and $currentKey -ne 'your-openai-api-key-here') { '✅ Configurada (' + $currentKey.Substring(0, 15) + '...)' } else { '❌ Não configurada' })" -ForegroundColor Cyan

# Se modo Validate
if ($Validate) {
    Write-Host "`n📋 Modo VALIDAÇÃO..." -ForegroundColor Cyan

    if ($currentKey -and $currentKey -ne 'your-openai-api-key-here') {
        Write-Host "`n1️⃣  Testando formato da chave..." -ForegroundColor Yellow
        if (-not (Test-ApiKeyFormat $currentKey)) {
            Write-Host "❌ Formato inválido" -ForegroundColor Red
            exit 1
        }
        Write-Host "✅ Formato válido" -ForegroundColor Green

        Write-Host "`n2️⃣  Testando chave com OpenAI..." -ForegroundColor Yellow
        if (-not (Test-ApiKey $currentKey)) {
            Write-Host "❌ Chave inválida" -ForegroundColor Red
            exit 1
        }

        Write-Host "`n3️⃣  Verificando Docker..." -ForegroundColor Yellow
        if (Test-Docker) {
            Write-Host "`n4️⃣  Verificando container..." -ForegroundColor Yellow
            Test-ContainerApiKey | Out-Null
        }

        Write-Host "`n✅ Validação concluída com sucesso!" -ForegroundColor Green
        exit 0
    } else {
        Write-Host "`n❌ Chave não configurada!" -ForegroundColor Red
        exit 1
    }
}

# Se modo Reset
if ($Reset) {
    Write-Host "`n🔄 Resetando configuração..." -ForegroundColor Yellow
    Update-EnvValue "OPENAI_API_KEY" "your-openai-api-key-here"
    Write-Host "✅ Configuração resetada" -ForegroundColor Green
    exit 0
}

# Se chave foi passada como argumento
if ($ApiKey) {
    Write-Host "`n📝 Configurando chave OpenAI..." -ForegroundColor Cyan

    if (-not (Test-ApiKeyFormat $ApiKey)) {
        Write-Host "❌ Formato de chave inválido!" -ForegroundColor Red
        Write-Host "Esperado: sk-proj-..." -ForegroundColor Yellow
        exit 1
    }

    Write-Host "✅ Formato válido" -ForegroundColor Green

    if (-not (Test-ApiKey $ApiKey)) {
        Write-Host "`n⚠️  Chave pode estar inválida. Deseja continuar?" -ForegroundColor Yellow
        $response = Read-Host "[S]im / [N]ão"
        if ($response -ne "S") {
            exit 1
        }
    }

    Update-EnvValue "OPENAI_API_KEY" $ApiKey

    if (Test-Docker) {
        Write-Host "`n❓ Deseja reiniciar os containers agora?" -ForegroundColor Yellow
        $response = Read-Host "[S]im / [N]ão"
        if ($response -eq "S") {
            Restart-Containers
        } else {
            Write-Host "Execute manualmente:" -ForegroundColor Yellow
            Write-Host "  cd docker && docker-compose restart ai-service backend" -ForegroundColor Cyan
        }
    } else {
        Write-Host "Execute quando pronto:" -ForegroundColor Yellow
        Write-Host "  cd docker && docker-compose up -d" -ForegroundColor Cyan
    }

    Write-Host "`n✅ Configuração concluída!" -ForegroundColor Green
    exit 0
}

# Modo interativo
Write-Host "`n🔧 Modo INTERATIVO..." -ForegroundColor Cyan

if ($currentKey -and $currentKey -ne 'your-openai-api-key-here') {
    Write-Host "`n Opções:" -ForegroundColor Yellow
    Write-Host "  1 - Validar chave atual" -ForegroundColor Cyan
    Write-Host "  2 - Configurar nova chave" -ForegroundColor Cyan
    Write-Host "  3 - Reset para padrão" -ForegroundColor Cyan
    Write-Host "  4 - Sair" -ForegroundColor Cyan

    $choice = Read-Host "`nEscolha"

    switch ($choice) {
        "1" {
            & $PSCommandPath -Validate
        }
        "2" {
            $newKey = Read-Host "`nDigite sua chave OpenAI"
            & $PSCommandPath -ApiKey $newKey
        }
        "3" {
            & $PSCommandPath -Reset
        }
        default {
            exit 0
        }
    }
} else {
    Write-Host "`n⚠️  Chave não está configurada!" -ForegroundColor Yellow
    Write-Host "`nDigite sua chave OpenAI (ou deixe em branco para sair):" -ForegroundColor Cyan
    Write-Host "Obtenha em: https://platform.openai.com/api-keys" -ForegroundColor Gray

    $newKey = Read-Host

    if ($newKey) {
        & $PSCommandPath -ApiKey $newKey
    } else {
        Write-Host "Abortado." -ForegroundColor Yellow
        exit 0
    }
}

