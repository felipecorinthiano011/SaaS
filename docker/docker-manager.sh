#!/bin/bash

# Resume Matcher SaaS - Docker Setup Helper Script
# This script helps manage Docker containers for the SaaS platform

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker Desktop."
        exit 1
    fi
    print_success "Docker is installed"
}

# Check if Docker is running
check_docker_running() {
    if ! docker ps &> /dev/null; then
        print_error "Docker is not running. Please start Docker."
        exit 1
    fi
    print_success "Docker is running"
}

# Setup environment
setup_env() {
    if [ ! -f .env ]; then
        print_info "Creating .env file from .env.example"
        cp .env.example .env
        print_success ".env created"
        print_warning "Please update .env with your configuration values"
    else
        print_info ".env already exists"
    fi
}

# Start services
start_services() {
    print_info "Starting Docker services..."
    docker compose up -d --build
    print_success "Services started"
}

# Stop services
stop_services() {
    print_info "Stopping Docker services..."
    docker compose down
    print_success "Services stopped"
}

# View logs
view_logs() {
    if [ $# -eq 0 ]; then
        docker compose logs -f
    else
        docker compose logs -f "$1"
    fi
}

# Check service health
check_health() {
    print_info "Checking service health..."

    # Check PostgreSQL
    if docker compose exec postgres pg_isready -U resume_user &> /dev/null; then
        print_success "PostgreSQL is healthy"
    else
        print_error "PostgreSQL is not healthy"
    fi

    # Check AI Service
    if curl -s http://localhost:8000/api/v1/keywords/health | grep -q "healthy"; then
        print_success "AI Service is healthy"
    else
        print_error "AI Service is not healthy"
    fi

    # Check Backend
    if curl -s http://localhost:8080/actuator/health | grep -q "UP"; then
        print_success "Backend is healthy"
    else
        print_error "Backend is not healthy"
    fi

    # Check Frontend
    if curl -s http://localhost:4200 &> /dev/null; then
        print_success "Frontend is healthy"
    else
        print_error "Frontend is not healthy"
    fi
}

# Clean up
cleanup() {
    print_warning "This will remove all containers, volumes, and networks."
    read -p "Are you sure? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker compose down -v
        print_success "Cleanup completed"
    else
        print_info "Cleanup cancelled"
    fi
}

# Show status
show_status() {
    print_info "Service Status:"
    docker compose ps
}

# Build images
build_images() {
    print_info "Building Docker images..."
    docker compose build --no-cache
    print_success "Images built successfully"
}

# Test database connection
test_db() {
    print_info "Testing database connection..."
    if docker compose exec postgres psql -U resume_user -d resume_optimizer -c "SELECT version();" &> /dev/null; then
        print_success "Database connection successful"
    else
        print_error "Database connection failed"
    fi
}

# Open web services
open_services() {
    print_info "Opening services in browser..."
    sleep 2

    if command -v open &> /dev/null; then
        # macOS
        open http://localhost:4200
        open http://localhost:8080
        open http://localhost:8000
    elif command -v xdg-open &> /dev/null; then
        # Linux
        xdg-open http://localhost:4200 &
        xdg-open http://localhost:8080 &
        xdg-open http://localhost:8000 &
    elif command -v start &> /dev/null; then
        # Windows
        start http://localhost:4200
        start http://localhost:8080
        start http://localhost:8000
    else
        print_info "Please open these URLs in your browser:"
        echo "  Frontend: http://localhost:4200"
        echo "  Backend: http://localhost:8080"
        echo "  AI Service: http://localhost:8000"
    fi
}

# Main menu
show_menu() {
    echo ""
    echo "========================================"
    echo "Resume Matcher SaaS - Docker Manager"
    echo "========================================"
    echo "1. Setup environment (.env)"
    echo "2. Start services"
    echo "3. Stop services"
    echo "4. View logs"
    echo "5. Check health"
    echo "6. Show status"
    echo "7. Build images"
    echo "8. Test database"
    echo "9. Open services in browser"
    echo "10. Cleanup (remove containers/volumes)"
    echo "0. Exit"
    echo "========================================"
}

# Main script
main() {
    # Check prerequisites
    check_docker
    check_docker_running

    if [ $# -eq 0 ]; then
        # Interactive mode
        while true; do
            show_menu
            read -p "Select an option (0-10): " choice

            case $choice in
                1) setup_env ;;
                2) start_services ;;
                3) stop_services ;;
                4) view_logs ;;
                5) check_health ;;
                6) show_status ;;
                7) build_images ;;
                8) test_db ;;
                9) open_services ;;
                10) cleanup ;;
                0) print_info "Exiting..."; exit 0 ;;
                *) print_error "Invalid option" ;;
            esac
        done
    else
        # Command mode
        case $1 in
            setup) setup_env ;;
            start) start_services ;;
            stop) stop_services ;;
            logs) view_logs $2 ;;
            health) check_health ;;
            status) show_status ;;
            build) build_images ;;
            test-db) test_db ;;
            open) open_services ;;
            clean) cleanup ;;
            *)
                echo "Usage: $0 {setup|start|stop|logs|health|status|build|test-db|open|clean}"
                exit 1
                ;;
        esac
    fi
}

main "$@"

