#!/bin/bash

# Script auxiliar para testar o sistema (Linux/Mac)
# Uso: chmod +x test-system.sh && ./test-system.sh

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

show_banner() {
    echo -e "${CYAN}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║         ResumeMatcher SaaS - Testing Toolkit          ║${NC}"
    echo -e "${CYAN}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

show_menu() {
    echo -e "${BLUE}┌────────────────────────────────────────────────────┐${NC}"
    echo -e "${BLUE}│           O que você deseja testar?               │${NC}"
    echo -e "${BLUE}└────────────────────────────────────────────────────┘${NC}"
    echo ""
    echo "1. ✅ Verificar Pré-requisitos (Node, Python, Java, Docker)"
    echo "2. 🐳 Iniciar todos os serviços com Docker Compose"
    echo "3. 🧪 Testar cada serviço individualmente"
    echo "4. 🌐 Testar endpoints da API"
    echo "5. 🔄 Teste End-to-End (fluxo completo)"
    echo "6. 📊 Ver status de todos os containers"
    echo "7. 📋 Ver logs em tempo real"
    echo "8. 🧹 Limpar tudo (parar containers)"
    echo "9. 🗑️  Resetar banco de dados"
    echo "0. ❌ Sair"
    echo ""
}

check_prerequisites() {
    echo -e "${YELLOW}🔍 Verificando pré-requisitos...${NC}"
    echo ""

    # Node.js
    echo -e "${CYAN}▶ Node.js:${NC}"
    if command -v node &> /dev/null; then
        version=$(node --version)
        echo -e "  ${GREEN}✅ Instalado: $version${NC}"
    else
        echo -e "  ${RED}❌ NÃO instalado (necessário para Frontend)${NC}"
    fi

    # Python
    echo -e "${CYAN}▶ Python:${NC}"
    if command -v python3 &> /dev/null; then
        version=$(python3 --version)
        echo -e "  ${GREEN}✅ Instalado: $version${NC}"
    else
        echo -e "  ${RED}❌ NÃO instalado (necessário para AI Service)${NC}"
    fi

    # Java
    echo -e "${CYAN}▶ Java:${NC}"
    if command -v java &> /dev/null; then
        version=$(java -version 2>&1 | head -1)
        echo -e "  ${GREEN}✅ Instalado: $version${NC}"
    else
        echo -e "  ${RED}❌ NÃO instalado (necessário para Backend)${NC}"
    fi

    # Docker
    echo -e "${CYAN}▶ Docker:${NC}"
    if command -v docker &> /dev/null; then
        version=$(docker --version)
        echo -e "  ${GREEN}✅ Instalado: $version${NC}"

        # Check Docker daemon
        if docker ps > /dev/null 2>&1; then
            echo -e "  ${GREEN}✅ Docker daemon está rodando${NC}"
        else
            echo -e "  ${YELLOW}⚠️  Docker não está rodando. Inicie o Docker!${NC}"
        fi
    else
        echo -e "  ${RED}❌ NÃO instalado (necessário para Database)${NC}"
    fi

    echo ""
    read -p "Pressione Enter para continuar..."
}

start_all_services() {
    echo -e "${GREEN}🚀 Iniciando todos os serviços com Docker Compose...${NC}"
    echo ""

    cd C:/Projects/Saas/docker

    echo -e "${CYAN}▶ Iniciando containers...${NC}"
    docker compose up --build

    cd -

    echo ""
    echo -e "${GREEN}✅ Serviços iniciados!${NC}"
    echo ""
    echo -e "${YELLOW}Acesse:${NC}"
    echo "  Frontend: http://localhost:4200"
    echo "  Backend: http://localhost:8080"
    echo "  AI Service: http://localhost:8000"
    echo "  Database: localhost:5432"
    echo ""
    read -p "Pressione Enter para voltar ao menu..."
}

test_services() {
    echo -e "${GREEN}🧪 Testando cada serviço...${NC}"
    echo ""

    # Test Database
    echo -e "${CYAN}1️⃣  Testando Database (PostgreSQL)...${NC}"
    if docker compose exec postgres pg_isready -U resume_user > /dev/null 2>&1; then
        echo -e "   ${GREEN}✅ Database está respondendo${NC}"
    else
        echo -e "   ${RED}❌ Database não está respondendo${NC}"
    fi

    # Test AI Service
    echo -e "${CYAN}2️⃣  Testando AI Service (FastAPI)...${NC}"
    if curl -s http://localhost:8000/api/v1/keywords/health > /dev/null 2>&1; then
        echo -e "   ${GREEN}✅ AI Service está respondendo${NC}"
    else
        echo -e "   ${RED}❌ AI Service não está respondendo (porta 8000)${NC}"
    fi

    # Test Backend
    echo -e "${CYAN}3️⃣  Testando Backend (Spring Boot)...${NC}"
    if curl -s http://localhost:8080/actuator/health > /dev/null 2>&1; then
        echo -e "   ${GREEN}✅ Backend está respondendo${NC}"
    else
        echo -e "   ${RED}❌ Backend não está respondendo (porta 8080)${NC}"
    fi

    # Test Frontend
    echo -e "${CYAN}4️⃣  Testando Frontend (Angular)...${NC}"
    if curl -s http://localhost:4200 > /dev/null 2>&1; then
        echo -e "   ${GREEN}✅ Frontend está respondendo${NC}"
    else
        echo -e "   ${RED}❌ Frontend não está respondendo (porta 4200)${NC}"
    fi

    echo ""
    read -p "Pressione Enter para continuar..."
}

test_apis() {
    echo -e "${GREEN}🌐 Testando Endpoints da API...${NC}"
    echo ""

    # Test Keywords Extract
    echo -e "${CYAN}1️⃣  Testando extraction de keywords...${NC}"

    response=$(curl -s -X POST \
        -H "Content-Type: application/json" \
        -d '{"job_description":"Senior Java Developer with Spring Boot and Docker"}' \
        http://localhost:8000/api/v1/keywords/extract)

    if [ ! -z "$response" ]; then
        echo -e "   ${GREEN}✅ Keywords extraídos com sucesso${NC}"
        echo "$response" | jq '.' 2>/dev/null || echo "$response"
    else
        echo -e "   ${RED}❌ Erro ao extrair keywords${NC}"
    fi

    echo ""
    echo -e "${CYAN}2️⃣  Testando health check...${NC}"

    response=$(curl -s http://localhost:8000/api/v1/keywords/health)

    if echo "$response" | grep -q "healthy"; then
        echo -e "   ${GREEN}✅ Health check OK${NC}"
    else
        echo -e "   ${RED}❌ Erro no health check${NC}"
    fi

    echo ""
    read -p "Pressione Enter para continuar..."
}

show_status() {
    echo -e "${GREEN}📊 Status dos Containers...${NC}"
    echo ""

    cd C:/Projects/Saas/docker
    docker compose ps
    cd -

    echo ""
    read -p "Pressione Enter para continuar..."
}

show_logs() {
    echo -e "${GREEN}📋 Logs em Tempo Real...${NC}"
    echo -e "${YELLOW}   (Pressione CTRL+C para parar)${NC}"
    echo ""

    cd C:/Projects/Saas/docker
    docker compose logs -f
    cd -
}

stop_all_services() {
    echo -e "${YELLOW}🧹 Parando todos os serviços...${NC}"
    echo ""

    cd C:/Projects/Saas/docker
    docker compose down
    cd -

    echo -e "${GREEN}✅ Serviços parados!${NC}"
    echo ""
    read -p "Pressione Enter para continuar..."
}

reset_database() {
    echo -e "${YELLOW}🗑️  Resetando banco de dados...${NC}"
    echo -e "${RED}   (Isso removerá TODOS os dados)${NC}"
    echo ""

    read -p "Tem certeza? (s/n): " confirm

    if [ "$confirm" = "s" ]; then
        cd C:/Projects/Saas/docker
        echo -e "${CYAN}Removendo volume do PostgreSQL...${NC}"
        docker compose down -v
        echo -e "${GREEN}✅ Banco resetado!${NC}"
        cd -
    else
        echo -e "${RED}❌ Operação cancelada${NC}"
    fi

    echo ""
    read -p "Pressione Enter para continuar..."
}

test_end_to_end() {
    echo -e "${GREEN}🔄 Teste End-to-End (Fluxo Completo)${NC}"
    echo ""
    echo -e "${YELLOW}Siga os passos abaixo:${NC}"
    echo ""

    echo -e "${CYAN}1️⃣  Abra o navegador:${NC}"
    echo "   http://localhost:4200"
    echo ""

    echo -e "${CYAN}2️⃣  Registre um novo usuário:${NC}"
    echo "   Email: test@example.com"
    echo "   Senha: password123"
    echo ""

    echo -e "${CYAN}3️⃣  Preencha o Job Description:${NC}"
    echo "   'Senior Java Developer with 5+ years experience'"
    echo ""

    echo -e "${CYAN}4️⃣  Preencha o Resume:${NC}"
    echo "   'JOHN DOE | Senior Developer | Java, Spring Boot, Docker'"
    echo ""

    echo -e "${CYAN}5️⃣  Clique 'Analyze & Optimize'${NC}"
    echo ""

    echo -e "${GREEN}✅ Verifique os resultados:${NC}"
    echo "   • ATS Score aparece"
    echo "   • Missing Keywords aparecem"
    echo "   • Suggestions aparecem"
    echo "   • Download funciona"
    echo ""

    read -p "Pressione Enter quando terminar o teste..."
}

# Main loop
while true; do
    clear
    show_banner
    show_menu

    read -p "Escolha uma opção (0-9): " choice

    case $choice in
        1) check_prerequisites ;;
        2) start_all_services ;;
        3) test_services ;;
        4) test_apis ;;
        5) test_end_to_end ;;
        6) show_status ;;
        7) show_logs ;;
        8) stop_all_services ;;
        9) reset_database ;;
        0)
            echo -e "${GREEN}👋 Até logo!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Opção inválida!${NC}"
            sleep 2
            ;;
    esac
done

