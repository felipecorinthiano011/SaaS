# Guia Completo - Testando o Sistema LocalMente

## 📋 Índice
1. [Pré-requisitos](#pré-requisitos)
2. [Setup Inicial](#setup-inicial)
3. [Iniciando os Serviços](#iniciando-os-serviços)
4. [Testando Cada Componente](#testando-cada-componente)
5. [Teste End-to-End](#teste-end-to-end)
6. [Troubleshooting](#troubleshooting)

---

## ✅ Pré-requisitos

Instale estas ferramentas:

### Windows (PowerShell)
```powershell
# 1. Verificar Node.js (para Frontend)
node --version
npm --version

# 2. Verificar Python (para AI Service)
python --version
pip --version

# 3. Verificar Java (para Backend)
java -version

# 4. Verificar Docker (para Database)
docker --version
docker ps
```

### Linux/Mac
```bash
node --version
npm --version
python3 --version
pip3 --version
java -version
docker --version
docker ps
```

**Versões Mínimas Requeridas**:
- Node.js: 18+
- Python: 3.11+
- Java: 21+
- Docker: 4.0+

---

## 🚀 Setup Inicial

### 1. Clonar Repositório (se necessário)
```bash
cd C:\Projects\Saas
```

### 2. Criar Arquivo .env
```bash
# Copiar template
copy .env.example .env

# Editar .env com suas credenciais
notepad .env
```

**Valores Mínimos para .env**:
```env
# Database
POSTGRES_DB=resume_optimizer
POSTGRES_USER=resume_user
POSTGRES_PASSWORD=password123

# Backend
JWT_SECRET=seu-secret-key-super-seguro-com-32-caracteres
AI_SERVICE_BASE_URL=http://localhost:8000

# AI Service
OPENAI_API_KEY=sk-seu-key-aqui (opcional para testes iniciais)
AI_DEBUG=true
```

### 3. Criar Estrutura de Pastas
```bash
# Já existe, apenas verificar:
cd C:\Projects\Saas
ls frontend/
ls backend/
ls ai-service/
ls docker/
```

---

## 🏗️ Iniciando os Serviços

### OPÇÃO 1: Usando Docker Compose (Recomendado)

**Terminal 1: Inicie todos os serviços**
```powershell
cd C:\Projects\Saas\docker

# Inicie com docker-compose
docker compose up --build

# Ou use o script helper
.\docker-manager.ps1
# Selecione opção 2: Start services
```

**Saída esperada**:
```
resume-optimizer-db      | PostgreSQL 16 running on port 5432
resume-optimizer-ai      | Uvicorn running on 0.0.0.0:8000
resume-optimizer-backend | Started on port 8080
resume-optimizer-frontend| Running on port 4200
```

**Verifique se todos estão rodando**:
```powershell
docker compose ps

# Resultado esperado:
NAME                        STATUS
resume-optimizer-db         Up
resume-optimizer-ai         Up
resume-optimizer-backend    Up
resume-optimizer-frontend   Up
```

---

### OPÇÃO 2: Iniciando Cada Serviço Manualmente

#### Terminal 1: Inicie o Database (PostgreSQL)
```powershell
cd C:\Projects\Saas\docker

docker compose up postgres

# Saída esperada:
# PostgreSQL is ready to accept connections
# Listening on port 5432
```

#### Terminal 2: Inicie o AI Service (FastAPI)
```powershell
cd C:\Projects\Saas\ai-service

# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Saída esperada:
# Uvicorn running on http://0.0.0.0:8000
# Press CTRL+C to quit
```

#### Terminal 3: Inicie o Backend (Spring Boot)
```powershell
cd C:\Projects\Saas\backend

# Windows/Linux/Mac (mesmo comando)
mvn spring-boot:run

# Saída esperada:
# Started ResumeMatcherApplication in X seconds
# Listening on port 8080
```

#### Terminal 4: Inicie o Frontend (Angular)
```powershell
cd C:\Projects\Saas\frontend

npm install  # Apenas primeira vez
ng serve

# Saída esperada:
# Application bundle generated successfully
# Listening on http://localhost:4200
```

---

## 🧪 Testando Cada Componente

### Teste 1: Verificar Database (PostgreSQL)

**Terminal Novo**:
```powershell
# Conectar ao banco
docker compose exec postgres psql -U resume_user -d resume_optimizer

# Dentro do psql:
\dt                          # Listar tabelas
SELECT * FROM pg_tables;     # Ver tabelas
\q                           # Sair
```

**Saída esperada**:
```
List of relations
Schema |      Name      | Type  |  Owner
--------+----------------+-------+-----------
 public | users          | table | resume_user
 public | resumes        | table | resume_user
 public | job_analyses   | table | resume_user
```

### Teste 2: Verificar AI Service (FastAPI)

**Via Browser**:
```
http://localhost:8000/docs
```

Você deve ver a documentação Swagger UI com todos os endpoints.

**Via cURL** (Terminal):
```powershell
# Teste endpoint de saúde
curl http://localhost:8000/api/v1/keywords/health

# Saída esperada:
# {"status":"healthy","service":"ats_keywords","version":"1.0.0"}
```

**Teste Extração de Keywords**:
```powershell
$body = @{
    job_description = "Senior Java Developer with Spring Boot and Docker experience"
} | ConvertTo-Json

Invoke-WebRequest -Method Post `
  -Uri http://localhost:8000/api/v1/keywords/extract `
  -ContentType "application/json" `
  -Body $body

# Saída esperada:
# {
#   "skills": ["Java", "Docker", ...],
#   "technologies": ["Spring Boot", ...],
#   "tools": [],
#   "soft_skills": []
# }
```

### Teste 3: Verificar Backend (Spring Boot)

**Via Browser**:
```
http://localhost:8080/actuator/health
```

**Saída esperada**:
```json
{
  "status": "UP",
  "components": {
    "db": {"status": "UP"},
    "diskSpace": {"status": "UP"}
  }
}
```

**Via cURL**:
```powershell
curl http://localhost:8080/actuator/health

# Saída esperada:
# {"status":"UP"}
```

### Teste 4: Verificar Frontend (Angular)

**Via Browser**:
```
http://localhost:4200
```

Você deve ver a página de login do ResumeMatcher.

---

## 🔄 Teste End-to-End (Fluxo Completo)

### Fluxo 1: Registrar Usuário

**1. Acesse o Frontend**:
```
http://localhost:4200
```

**2. Clique em "Sign up"**

**3. Preencha o formulário**:
```
Full Name: Test User
Email: test@example.com
Password: password123
Confirm Password: password123
```

**4. Clique em "Create Account"**

**Resultado esperado**:
- ✅ Registrado com sucesso
- ✅ Redirecionado para Dashboard
- ✅ Vê o email na barra superior

### Fluxo 2: Fazer Login

**1. Faça Logout** (botão vermelho canto superior)

**2. Clique em "Sign in"**

**3. Preencha credenciais**:
```
Email: test@example.com
Password: password123
```

**4. Clique em "Sign In"**

**Resultado esperado**:
- ✅ Login bem-sucedido
- ✅ Redirecionado para Dashboard
- ✅ Vê o email no header

### Fluxo 3: Analisar Resume

**1. No Dashboard, preencha "Job Description"**:
```
Senior Java Developer with 5+ years experience.
Required Skills: Java, Spring Boot, Docker, Kubernetes, PostgreSQL.
Experience with microservices architecture.
Strong communication and leadership skills required.
```

**2. Preencha "Your Resume"** (opção: colar texto):
```
JOHN DOE
Senior Software Engineer

EXPERIENCE
Senior Developer at TechCorp (2020-Present)
- Developed Java microservices with Spring Boot
- Used Docker for containerization
- Managed PostgreSQL databases
- Led team of 3 developers

EDUCATION
BS Computer Science, State University (2015)

SKILLS
Java, Python, Spring Framework, Docker, Git
```

**3. Clique em "Analyze & Optimize"**

**Resultado esperado**:
- ✅ Tab muda para "Results"
- ✅ ATS Score aparece (ex: 75/100)
- ✅ Missing Keywords aparece
- ✅ Suggestions aparece
- ✅ Optimized Resume está disponível

### Fluxo 4: Download Resume Otimizado

**1. Na seção "Optimized Resume"**

**2. Clique em "Download"**

**Resultado esperado**:
- ✅ Arquivo "optimized-resume.txt" baixado
- ✅ Contém resume otimizado

---

## 📊 Testes Adicionais (Opcional)

### Teste de API com Postman/Insomnia

**Crie uma requisição POST**:
```
URL: http://localhost:8000/api/v1/resume/optimize

Body (JSON):
{
  "job_description": "Senior Java Developer...",
  "resume_text": "JOHN DOE..."
}

Headers:
Content-Type: application/json
```

**Resultado esperado**:
```json
{
  "ats_score": 75,
  "missing_keywords": ["Kubernetes", "Communication"],
  "optimized_resume": "...",
  "suggestions": [...]
}
```

### Teste de Otimização de Tokens

**1. Ative debug logging**:
```
Edite .env:
AI_DEBUG=true
```

**2. Monitore os logs**:
```powershell
docker compose logs ai-service | Select-String "Original|Optimized|Savings"
```

**3. Você verá**:
```
Original: 2500 chars -> Optimized: 1000 chars (60% reduction)
Original: 1500 chars -> Optimized: 600 chars (60% reduction)
```

---

## 🐛 Troubleshooting

### Erro: "Port already in use"

```powershell
# Encontre o processo usando a porta
netstat -ano | findstr :8000
netstat -ano | findstr :8080
netstat -ano | findstr :4200
netstat -ano | findstr :5432

# Mate o processo (substitua PID)
taskkill /PID <PID> /F

# Ou use portas diferentes:
ng serve --port 4300
uvicorn app.main:app --port 8001
```

### Erro: "Could not connect to PostgreSQL"

```powershell
# Verifique se container está rodando
docker ps | findstr postgres

# Se não está, reinicie:
docker compose up postgres -d

# Teste conexão:
docker compose exec postgres psql -U resume_user -c "SELECT 1"
```

### Erro: "CORS Error"

```
Certifique-se que o backend está rodando na porta 8080
Verifique CORS settings no backend (SecurityConfig.java)
```

### Erro: "Module not found (Python)"

```powershell
# Reinstale dependências
cd ai-service
pip install -r requirements.txt --upgrade

# Ou use venv limpo
rmdir .venv /s
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Erro: "Maven build fails"

```powershell
# Limpe cache Maven
cd backend
mvn clean

# Rebuild
mvn package

# Se ainda falhar, verifique Java version
java -version
```

### Frontend não carrega em localhost:4200

```powershell
# Verifique se ng serve está rodando
# Se não:
cd frontend
npm install
ng serve

# Ou se tiver erro de Angular CLI:
npm install -g @angular/cli@latest
ng serve
```

---

## ✅ Checklist de Testes

Use este checklist para validar tudo:

```
DATABASE
  ☐ Docker container está rodando
  ☐ Consegue conectar com psql
  ☐ Tabelas foram criadas
  
AI SERVICE
  ☐ Uvicorn está rodando na porta 8000
  ☐ Endpoint /health retorna 200
  ☐ Swagger UI acessível em /docs
  ☐ Endpoint /keywords/extract funciona
  
BACKEND
  ☐ Spring Boot iniciou sem erros
  ☐ Listening na porta 8080
  ☐ /actuator/health retorna UP
  ☐ Banco conectado com sucesso
  
FRONTEND
  ☐ Angular app rodando na porta 4200
  ☐ Página de login carrega
  ☐ Registro funciona
  ☐ Login funciona
  ☐ Dashboard carrega
  
FLUXO END-TO-END
  ☐ Registrar novo usuário
  ☐ Fazer login
  ☐ Analisar resume
  ☐ Ver ATS score
  ☐ Ver suggestions
  ☐ Download resume otimizado
```

---

## 🎯 Próximos Passos Após Testes

Se tudo passou nos testes:

1. **Explorar a UI**:
   - Teste múltiplas análises
   - Experimente diferentes resumes
   - Verifique diferentes job descriptions

2. **Verificar Logs**:
   ```powershell
   docker compose logs backend  # Ver logs do backend
   docker compose logs ai-service  # Ver logs da AI
   ```

3. **Monitorar Performance**:
   ```powershell
   docker stats  # Ver CPU/Memory usage
   ```

4. **Fazer Commits**:
   ```bash
   git add .
   git commit -m "Testing complete - all services working"
   ```

5. **Deploy** (próximo passo):
   - Vercel (frontend)
   - Heroku/Railway (backend)
   - AWS Lambda (AI service)

---

## 📞 Comandos Úteis

```powershell
# Ver todos os containers
docker compose ps

# Ver logs em tempo real
docker compose logs -f

# Parar tudo
docker compose down

# Parar tudo e remover volumes
docker compose down -v

# Rebuild tudo
docker compose build --no-cache

# Executar comando no container
docker compose exec backend bash

# Limpar sistema Docker
docker system prune -a
```

---

## 🎓 Estrutura de Pastas para Teste

```
C:\Projects\Saas\
├── frontend/          ← ng serve (porta 4200)
├── backend/           ← mvn spring-boot:run (porta 8080)
├── ai-service/        ← uvicorn (porta 8000)
├── docker/            ← docker-compose.yml
│   └── docker-manager.ps1  ← Helper script
├── .env               ← Suas credenciais
└── README.md          ← Este guia
```

---

## ✨ Dicas Finais

1. **Mantenha 4 terminais abertos**:
   - Terminal 1: Docker Compose (todos os serviços)
   - Terminal 2: Logs (docker compose logs -f)
   - Terminal 3: Browser (http://localhost:4200)
   - Terminal 4: cURL/Postman para testes

2. **Use Docker Compose** (mais fácil que rodar tudo manualmente)

3. **Verifique as portas**:
   - Frontend: 4200
   - Backend: 8080
   - AI Service: 8000
   - Database: 5432

4. **Guarde os logs** em caso de problemas

5. **Teste com dados reais** (job descriptions e resumes reais)

---

**Data**: 5 de Abril de 2026  
**Status**: ✅ Pronto para Testes Completos

