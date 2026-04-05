# Script auxiliar para testar o sistema
# Uso: .\test-system.ps1

Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║         ResumeMatcher SaaS - Testing Toolkit          ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

function Show-Menu {
    Write-Host "┌────────────────────────────────────────────────────┐" -ForegroundColor Blue
    Write-Host "│           O que você deseja testar?               │" -ForegroundColor Blue
    Write-Host "└────────────────────────────────────────────────────┘" -ForegroundColor Blue
    Write-Host ""
    Write-Host "1. ✅ Verificar Pré-requisitos (Node, Python, Java, Docker)"
    Write-Host "2. 🐳 Iniciar todos os serviços com Docker Compose"
    Write-Host "3. 🧪 Testar cada serviço individualmente"
    Write-Host "4. 🌐 Testar endpoints da API"
    Write-Host "5. 🔄 Teste End-to-End (fluxo completo)"
    Write-Host "6. 📊 Ver status de todos os containers"
    Write-Host "7. 📋 Ver logs em tempo real"
    Write-Host "8. 🧹 Limpar tudo (parar containers)"
    Write-Host "9. 🗑️  Resetar banco de dados"
    Write-Host "0. ❌ Sair"
    Write-Host ""
}

function Check-Prerequisites {
    Write-Host "🔍 Verificando pré-requisitos..." -ForegroundColor Yellow
    Write-Host ""

    # Node.js
    Write-Host "▶ Node.js:" -ForegroundColor Cyan
    if (Get-Command node -ErrorAction SilentlyContinue) {
        $version = node --version
        Write-Host "  ✅ Instalado: $version" -ForegroundColor Green
    } else {
        Write-Host "  ❌ NÃO instalado (necessário para Frontend)" -ForegroundColor Red
    }

    # Python
    Write-Host "▶ Python:" -ForegroundColor Cyan
    if (Get-Command python -ErrorAction SilentlyContinue) {
        $version = python --version
        Write-Host "  ✅ Instalado: $version" -ForegroundColor Green
    } else {
        Write-Host "  ❌ NÃO instalado (necessário para AI Service)" -ForegroundColor Red
    }

    # Java
    Write-Host "▶ Java:" -ForegroundColor Cyan
    if (Get-Command java -ErrorAction SilentlyContinue) {
        $version = java -version 2>&1 | Select-Object -First 1
        Write-Host "  ✅ Instalado: $version" -ForegroundColor Green
    } else {
        Write-Host "  ❌ NÃO instalado (necessário para Backend)" -ForegroundColor Red
    }

    # Docker
    Write-Host "▶ Docker:" -ForegroundColor Cyan
    if (Get-Command docker -ErrorAction SilentlyContinue) {
        $version = docker --version
        Write-Host "  ✅ Instalado: $version" -ForegroundColor Green

        # Verificar Docker daemon
        try {
            $null = docker ps
            Write-Host "  ✅ Docker daemon está rodando" -ForegroundColor Green
        } catch {
            Write-Host "  ⚠️  Docker não está rodando. Inicie o Docker Desktop!" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  ❌ NÃO instalado (necessário para Database)" -ForegroundColor Red
    }

    Write-Host ""
    Read-Host "Pressione Enter para continuar"
}

function Start-AllServices {
    Write-Host "🚀 Iniciando todos os serviços com Docker Compose..." -ForegroundColor Green
    Write-Host ""

    Push-Location "C:\Projects\Saas\docker"

    Write-Host "▶ Iniciando containers..." -ForegroundColor Cyan
    docker compose up --build

    Pop-Location

    Write-Host ""
    Write-Host "✅ Serviços iniciados!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Acesse:" -ForegroundColor Yellow
    Write-Host "  Frontend: http://localhost:4200"
    Write-Host "  Backend: http://localhost:8080"
    Write-Host "  AI Service: http://localhost:8000"
    Write-Host "  Database: localhost:5432"
    Write-Host ""
    Read-Host "Pressione Enter para voltar ao menu"
}

function Test-Services {
    Write-Host "🧪 Testando cada serviço..." -ForegroundColor Green
    Write-Host ""

    # Test Database
    Write-Host "1️⃣  Testando Database (PostgreSQL)..." -ForegroundColor Cyan
    try {
        $result = docker compose exec postgres pg_isready -U resume_user
        Write-Host "   ✅ Database está respondendo" -ForegroundColor Green
    } catch {
        Write-Host "   ❌ Database não está respondendo" -ForegroundColor Red
    }

    # Test AI Service
    Write-Host "2️⃣  Testando AI Service (FastAPI)..." -ForegroundColor Cyan
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/keywords/health" -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "   ✅ AI Service está respondendo" -ForegroundColor Green
        }
    } catch {
        Write-Host "   ❌ AI Service não está respondendo (porta 8000)" -ForegroundColor Red
        Write-Host "      Verifique se está rodando: docker compose logs ai-service" -ForegroundColor Yellow
    }

    # Test Backend
    Write-Host "3️⃣  Testando Backend (Spring Boot)..." -ForegroundColor Cyan
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8080/actuator/health" -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "   ✅ Backend está respondendo" -ForegroundColor Green
        }
    } catch {
        Write-Host "   ❌ Backend não está respondendo (porta 8080)" -ForegroundColor Red
        Write-Host "      Verifique se está rodando: mvn spring-boot:run" -ForegroundColor Yellow
    }

    # Test Frontend
    Write-Host "4️⃣  Testando Frontend (Angular)..." -ForegroundColor Cyan
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:4200" -ErrorAction Stop
        Write-Host "   ✅ Frontend está respondendo" -ForegroundColor Green
    } catch {
        Write-Host "   ❌ Frontend não está respondendo (porta 4200)" -ForegroundColor Red
        Write-Host "      Verifique se está rodando: ng serve" -ForegroundColor Yellow
    }

    Write-Host ""
    Read-Host "Pressione Enter para continuar"
}

function Test-APIs {
    Write-Host "🌐 Testando Endpoints da API..." -ForegroundColor Green
    Write-Host ""

    # Test Keywords Extract
    Write-Host "1️⃣  Testando extraction de keywords..." -ForegroundColor Cyan
    $body = @{
        job_description = "Senior Java Developer with Spring Boot and Docker"
    } | ConvertTo-Json

    try {
        $response = Invoke-WebRequest -Method Post `
            -Uri "http://localhost:8000/api/v1/keywords/extract" `
            -ContentType "application/json" `
            -Body $body `
            -ErrorAction Stop

        $result = $response.Content | ConvertFrom-Json
        Write-Host "   ✅ Keywords extraídos com sucesso:" -ForegroundColor Green
        Write-Host "      Skills: $($result.skills -join ', ')" -ForegroundColor Gray
        Write-Host "      Technologies: $($result.technologies -join ', ')" -ForegroundColor Gray
    } catch {
        Write-Host "   ❌ Erro ao extrair keywords" -ForegroundColor Red
    }

    Write-Host ""
    Write-Host "2️⃣  Testando health check..." -ForegroundColor Cyan
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/keywords/health" -ErrorAction Stop
        $result = $response.Content | ConvertFrom-Json
        Write-Host "   ✅ Health check OK" -ForegroundColor Green
        Write-Host "      Status: $($result.status)" -ForegroundColor Gray
    } catch {
        Write-Host "   ❌ Erro no health check" -ForegroundColor Red
    }

    Write-Host ""
    Read-Host "Pressione Enter para continuar"
}

function Show-Status {
    Write-Host "📊 Status dos Containers..." -ForegroundColor Green
    Write-Host ""

    Push-Location "C:\Projects\Saas\docker"
    docker compose ps
    Pop-Location

    Write-Host ""
    Read-Host "Pressione Enter para continuar"
}

function Show-Logs {
    Write-Host "📋 Logs em Tempo Real..." -ForegroundColor Green
    Write-Host "   (Pressione CTRL+C para parar)" -ForegroundColor Yellow
    Write-Host ""

    Push-Location "C:\Projects\Saas\docker"
    docker compose logs -f
    Pop-Location
}

function Stop-AllServices {
    Write-Host "🧹 Parando todos os serviços..." -ForegroundColor Yellow
    Write-Host ""

    Push-Location "C:\Projects\Saas\docker"
    docker compose down
    Pop-Location

    Write-Host "✅ Serviços parados!" -ForegroundColor Green
    Write-Host ""
    Read-Host "Pressione Enter para continuar"
}

function Reset-Database {
    Write-Host "🗑️  Resetando banco de dados..." -ForegroundColor Yellow
    Write-Host "   (Isso removerá TODOS os dados)" -ForegroundColor Red
    Write-Host ""

    $confirm = Read-Host "Tem certeza? (s/n)"

    if ($confirm -eq "s") {
        Push-Location "C:\Projects\Saas\docker"
        Write-Host "Removendo volume do PostgreSQL..." -ForegroundColor Cyan
        docker compose down -v
        Write-Host "✅ Banco resetado!" -ForegroundColor Green
        Pop-Location
    } else {
        Write-Host "❌ Operação cancelada" -ForegroundColor Red
    }

    Write-Host ""
    Read-Host "Pressione Enter para continuar"
}

function Test-EndToEnd {
    Write-Host "🔄 Teste End-to-End (Fluxo Completo)" -ForegroundColor Green
    Write-Host ""
    Write-Host "Siga os passos abaixo:" -ForegroundColor Yellow
    Write-Host ""

    Write-Host "1️⃣  Abra o navegador:" -ForegroundColor Cyan
    Write-Host "   http://localhost:4200" -ForegroundColor White
    Write-Host ""

    Write-Host "2️⃣  Registre um novo usuário:" -ForegroundColor Cyan
    Write-Host "   Email: test@example.com" -ForegroundColor Gray
    Write-Host "   Senha: password123" -ForegroundColor Gray
    Write-Host ""

    Write-Host "3️⃣  Preencha o Job Description:" -ForegroundColor Cyan
    Write-Host "   'Senior Java Developer with 5+ years experience'" -ForegroundColor Gray
    Write-Host ""

    Write-Host "4️⃣  Preencha o Resume:" -ForegroundColor Cyan
    Write-Host "   'JOHN DOE | Senior Developer | Java, Spring Boot, Docker'" -ForegroundColor Gray
    Write-Host ""

    Write-Host "5️⃣  Clique 'Analyze & Optimize'" -ForegroundColor Cyan
    Write-Host ""

    Write-Host "✅ Verifique os resultados:" -ForegroundColor Green
    Write-Host "   • ATS Score aparece" -ForegroundColor Gray
    Write-Host "   • Missing Keywords aparecem" -ForegroundColor Gray
    Write-Host "   • Suggestions aparecem" -ForegroundColor Gray
    Write-Host "   • Download funciona" -ForegroundColor Gray
    Write-Host ""

    Read-Host "Pressione Enter quando terminar o teste"
}

# Main loop
while ($true) {
    Clear-Host
    Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║         ResumeMatcher SaaS - Testing Toolkit          ║" -ForegroundColor Cyan
    Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""

    Show-Menu

    $choice = Read-Host "Escolha uma opção (0-9)"

    switch ($choice) {
        "1" { Check-Prerequisites }
        "2" { Start-AllServices }
        "3" { Test-Services }
        "4" { Test-APIs }
        "5" { Test-EndToEnd }
        "6" { Show-Status }
        "7" { Show-Logs }
        "8" { Stop-AllServices }
        "9" { Reset-Database }
        "0" {
            Write-Host "👋 Até logo!" -ForegroundColor Green
            exit
        }
        default {
            Write-Host "❌ Opção inválida!" -ForegroundColor Red
            Start-Sleep -Seconds 2
        }
    }
}

