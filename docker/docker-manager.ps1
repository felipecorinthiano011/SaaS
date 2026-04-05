# Resume Matcher SaaS - Docker Manager (PowerShell)
# This script helps manage Docker containers for the SaaS platform

param(
    [Parameter(Position=0)]
    [ValidateSet('setup', 'start', 'stop', 'logs', 'health', 'status', 'build', 'test-db', 'open', 'clean')]
    [string]$Command,

    [Parameter(Position=1)]
    [string]$Service = ''
)

# Color functions
function Write-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ $Message" -ForegroundColor Cyan
}

function Write-Warning-Custom {
    param([string]$Message)
    Write-Host "⚠ $Message" -ForegroundColor Yellow
}

# Check if Docker is running
function Check-Docker {
    try {
        $null = docker ps 2>$null
        Write-Success "Docker is running"
    }
    catch {
        Write-Error-Custom "Docker is not running. Please start Docker Desktop."
        exit 1
    }
}

# Setup environment
function Setup-Env {
    if (-not (Test-Path ".env")) {
        Write-Info "Creating .env file from .env.example"
        Copy-Item ".env.example" ".env"
        Write-Success ".env created"
        Write-Warning-Custom "Please update .env with your configuration values"
    }
    else {
        Write-Info ".env already exists"
    }
}

# Start services
function Start-Services {
    Write-Info "Starting Docker services..."
    docker compose up -d --build
    Write-Success "Services started"

    Write-Info "Waiting for services to be ready..."
    Start-Sleep -Seconds 5

    Write-Info "Services running at:"
    Write-Host "  Frontend:   http://localhost:4200" -ForegroundColor Green
    Write-Host "  Backend:    http://localhost:8080" -ForegroundColor Green
    Write-Host "  AI Service: http://localhost:8000" -ForegroundColor Green
}

# Stop services
function Stop-Services {
    Write-Info "Stopping Docker services..."
    docker compose down
    Write-Success "Services stopped"
}

# View logs
function View-Logs {
    param([string]$Service)

    if ($Service) {
        docker compose logs -f $Service
    }
    else {
        docker compose logs -f
    }
}

# Check service health
function Check-Health {
    Write-Info "Checking service health..."
    Write-Host ""

    # PostgreSQL
    try {
        $null = docker compose exec postgres pg_isready -U resume_user 2>$null
        Write-Success "PostgreSQL is healthy"
    }
    catch {
        Write-Error-Custom "PostgreSQL is not healthy"
    }

    # AI Service
    try {
        $response = curl.exe -s http://localhost:8000/api/v1/keywords/health
        if ($response -like "*healthy*") {
            Write-Success "AI Service is healthy"
        }
        else {
            Write-Error-Custom "AI Service is not responding correctly"
        }
    }
    catch {
        Write-Error-Custom "AI Service is not responding"
    }

    # Backend
    try {
        $response = curl.exe -s http://localhost:8080/actuator/health
        if ($response -like "*UP*") {
            Write-Success "Backend is healthy"
        }
        else {
            Write-Error-Custom "Backend is not responding correctly"
        }
    }
    catch {
        Write-Error-Custom "Backend is not responding"
    }

    # Frontend
    try {
        $null = curl.exe -s http://localhost:4200 2>$null
        Write-Success "Frontend is running"
    }
    catch {
        Write-Error-Custom "Frontend is not responding"
    }

    Write-Host ""
}

# Show status
function Show-Status {
    Write-Info "Service Status:"
    Write-Host ""
    docker compose ps
    Write-Host ""
}

# Build images
function Build-Images {
    Write-Info "Building Docker images..."
    docker compose build --no-cache
    Write-Success "Images built successfully"
}

# Test database connection
function Test-Database {
    Write-Info "Testing database connection..."
    try {
        $result = docker compose exec postgres psql -U resume_user -d resume_optimizer -c "SELECT version();" 2>$null
        Write-Success "Database connection successful"
        Write-Host $result -ForegroundColor Gray
    }
    catch {
        Write-Error-Custom "Database connection failed"
    }
}

# Open services in browser
function Open-Services {
    Write-Info "Opening services in browser..."
    Start-Sleep -Seconds 2

    try {
        Start-Process "http://localhost:4200"
        Start-Process "http://localhost:8080"
        Start-Process "http://localhost:8000"
    }
    catch {
        Write-Warning-Custom "Could not open browser automatically"
        Write-Host "Please open these URLs manually:" -ForegroundColor Yellow
        Write-Host "  Frontend:   http://localhost:4200"
        Write-Host "  Backend:    http://localhost:8080"
        Write-Host "  AI Service: http://localhost:8000"
    }
}

# Cleanup
function Cleanup-Docker {
    Write-Warning-Custom "This will remove all containers, volumes, and networks."
    $confirm = Read-Host "Are you sure? (y/n)"

    if ($confirm -eq 'y') {
        docker compose down -v
        Write-Success "Cleanup completed"
    }
    else {
        Write-Info "Cleanup cancelled"
    }
}

# Show menu
function Show-Menu {
    Write-Host ""
    Write-Host "========================================"  -ForegroundColor Cyan
    Write-Host "Resume Matcher SaaS - Docker Manager"    -ForegroundColor Cyan
    Write-Host "========================================"  -ForegroundColor Cyan
    Write-Host "1. Setup environment (.env)"             -ForegroundColor White
    Write-Host "2. Start services"                       -ForegroundColor White
    Write-Host "3. Stop services"                        -ForegroundColor White
    Write-Host "4. View logs"                            -ForegroundColor White
    Write-Host "5. Check health"                         -ForegroundColor White
    Write-Host "6. Show status"                          -ForegroundColor White
    Write-Host "7. Build images"                         -ForegroundColor White
    Write-Host "8. Test database"                        -ForegroundColor White
    Write-Host "9. Open services in browser"             -ForegroundColor White
    Write-Host "10. Cleanup (remove containers/volumes)" -ForegroundColor White
    Write-Host "0. Exit"                                 -ForegroundColor White
    Write-Host "========================================"  -ForegroundColor Cyan
}

# Main function
function Main {
    Check-Docker

    if ($Command) {
        # Command mode
        switch ($Command) {
            'setup' { Setup-Env }
            'start' { Start-Services }
            'stop' { Stop-Services }
            'logs' { View-Logs -Service $Service }
            'health' { Check-Health }
            'status' { Show-Status }
            'build' { Build-Images }
            'test-db' { Test-Database }
            'open' { Open-Services }
            'clean' { Cleanup-Docker }
            default { Write-Error-Custom "Unknown command: $Command" }
        }
    }
    else {
        # Interactive mode
        while ($true) {
            Show-Menu
            $choice = Read-Host "Select an option (0-10)"

            switch ($choice) {
                '1' { Setup-Env }
                '2' { Start-Services }
                '3' { Stop-Services }
                '4' { View-Logs }
                '5' { Check-Health }
                '6' { Show-Status }
                '7' { Build-Images }
                '8' { Test-Database }
                '9' { Open-Services }
                '10' { Cleanup-Docker }
                '0' { Write-Info "Exiting..."; exit 0 }
                default { Write-Error-Custom "Invalid option" }
            }

            Write-Host ""
            Read-Host "Press Enter to continue"
        }
    }
}

# Run main
Main

