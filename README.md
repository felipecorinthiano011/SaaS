# LinkedIn Resume Optimizer SaaS

Uma plataforma SaaS completa que analisa descrições de vagas do LinkedIn e otimiza resumes usando IA para melhorar o match com a vaga desejada.

## 🎯 Visão Geral

O LinkedIn Resume Optimizer é uma aplicação full-stack que ajuda candidatos a adaptarem seus resumes para vagas específicas através de análise de keywords ATS, sugestões de melhorias e geração de versões otimizadas do documento.

### Fluxo Principal

1. **Autenticação**: Usuário se registra/faz login (autenticação JWT)
2. **Envio de Dados**: Usuário cola a descrição da vaga do LinkedIn e faz upload do resume (PDF ou DOCX)
3. **Processamento**: Backend envia dados para o AI Service
4. **Análise IA**: Extração de keywords ATS, análise de match, otimização do resume
5. **Resultados**: Exibição de score ATS, keywords faltantes, sugestões e download do resume otimizado

---

## 🏗️ Arquitetura

O projeto é organizado em 4 componentes principais:

### **Frontend** (`/frontend`)
- **Stack**: Angular 17+ com TailwindCSS
- **Recursos**: 
  - Autenticação JWT
  - Upload de resumes (PDF/DOCX)
  - Formulário para colar job description
  - Visualização de resultados com ATS score, keywords, sugestões
  - Download de resume otimizado
- **Deploy**: Vercel

### **Backend** (`/backend`)
- **Stack**: Spring Boot 3 com Java 21
- **Recursos**:
  - API REST com autenticação JWT
  - Banco de dados PostgreSQL com JPA/Hibernate
  - Integração com AI Service
  - Persistência de análises
  - Clean Architecture (Controllers → Services → Repositories)
- **Entities**:
  - `User`: Informações do usuário
  - `Resume`: Arquivo e texto extraído
  - `JobAnalysis`: Resultados da análise (score, keywords, resume otimizado)
- **Deploy**: Railway (Docker)

### **AI Service** (`/ai-service`)
- **Stack**: Python FastAPI + LangChain + OpenAI API
- **Recursos**:
  - Extração de keywords ATS da job description
  - Parsing de resumes PDF/DOCX
  - Análise de match entre resume e vaga
  - Cálculo de ATS score
  - Otimização e reescrita de resume
  - Sugestões de melhorias
- **Deploy**: Railway (Docker)

### **Infrastructure** (`/docker`)
- Docker Compose para orquestração local
- Dockerfiles para cada serviço
- Volume para persistência PostgreSQL
- Network interna entre serviços

---

## 🚀 Quick Start Local

### Pré-requisitos
- **Docker** e **Docker Compose** instalados
- **OpenAI API Key** (obtenha em https://platform.openai.com/api-keys)
- **.env** configurado na raiz do projeto

### 1. Configurar Variáveis de Ambiente

Crie/edite o arquivo `.env` na raiz do projeto:

```env
# Database Configuration
POSTGRES_DB=resume_optimizer
POSTGRES_USER=resume_user
POSTGRES_PASSWORD=resume_password

# Backend Configuration
JWT_SECRET=cmVwbGFjZV93aXRoX2F0X2xlYXN0XzMyX2NoYXJzX2Jhc2U2NF9zZWNyZXQ=
JWT_EXPIRATION_SECONDS=3600

# AI Service Configuration (OBRIGATÓRIO)
OPENAI_API_KEY=sk-proj-sua-chave-aqui
AI_LLM_NAME=gpt-4o-mini
AI_DEBUG=false
AI_MINIMUM_KEYWORD_COUNT=15

# Spring Configuration
SPRING_JPA_HIBERNATE_DDL_AUTO=update
SPRING_JPA_SHOW_SQL=false
```

### 2. Iniciar os Serviços

```powershell
cd docker
docker compose up --build
```

### 3. Acessar a Aplicação

- **Frontend**: http://localhost:4200
- **Backend API**: http://localhost:8080/api
- **Backend Health**: http://localhost:8080/api/health
- **AI Service Docs**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432

### 4. Dados de Teste

#### Criar usuário de teste (via psql)
```sql
-- Conectar ao container do banco
docker exec -it resume-optimizer-db psql -U resume_user -d resume_optimizer

-- Inserir usuário de teste
INSERT INTO "user" (email, password, created_at) 
VALUES ('test@example.com', '$2a$10$...bcrypted_password...', NOW());
```

#### Credenciais de teste
- **Email**: test@example.com
- **Senha**: Test@1234

---

## 📋 Endpoints da API

### Autenticação

```
POST /api/auth/register
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}

POST /api/auth/login
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

### Resumes

```
POST /api/resume/upload
Content-Type: multipart/form-data
- file: [PDF/DOCX file]

GET /api/resume/{id}
```

### Análise de Vagas

```
POST /api/job/analyze
{
  "jobDescription": "Senior Java Developer...",
  "resumeText": "John Doe\nExperienced developer..."
}

Response:
{
  "atsScore": 78,
  "missingKeywords": ["Docker", "Kubernetes"],
  "optimizedResume": "...",
  "suggestions": [
    "Adicionar experiência com containers",
    "Destacar projetos em cloud"
  ]
}

GET /api/analysis/{id}
GET /api/analysis
```

---

## 🔧 Desenvolvimento Local (sem Docker)

### Backend (Spring Boot)

```bash
cd backend
mvn clean install
mvn spring-boot:run
```

Requisitos: Java 21, Maven 3.9+

### Frontend (Angular)

```bash
cd frontend
npm install
ng serve
```

Acesse: http://localhost:4200
Requisitos: Node 20+, Angular CLI

### AI Service (Python)

```bash
cd ai-service
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

Requisitos: Python 3.11+
Docs: http://localhost:8000/docs

---

## 🐳 Docker Compose

### Iniciar serviços
```bash
cd docker
docker compose up --build
```

### Parar serviços
```bash
docker compose down
```

### Ver logs
```bash
docker compose logs -f [service-name]
# Exemplos: backend, ai-service, postgres, frontend
```

### Reconstruir uma imagem
```bash
docker compose up --build [service-name]
```

---

## 📦 Estrutura de Pastas

```
C:\Projects\Saas/
├── frontend/                 # Angular app
│   ├── src/
│   │   ├── app/
│   │   │   ├── features/    # Páginas (auth, dashboard)
│   │   │   ├── shared/      # Componentes/serviços compartilhados
│   │   │   └── core/        # Interceptores, guards
│   │   └── environments/
│   └── package.json
│
├── backend/                  # Spring Boot API
│   ├── src/main/java/
│   │   └── com/saas/resumematcher/
│   │       ├── controller/   # REST endpoints
│   │       ├── service/      # Lógica de negócio
│   │       ├── repository/   # JPA repositories
│   │       ├── entity/       # Modelos JPA
│   │       ├── dto/          # Data Transfer Objects
│   │       ├── security/     # JWT, segurança
│   │       └── config/       # Configurações
│   ├── src/test/
│   └── pom.xml
│
├── ai-service/               # FastAPI service
│   ├── app/
│   │   ├── main.py          # Entry point
│   │   ├── routers/         # Endpoints
│   │   ├── services/        # Lógica de análise
│   │   ├── schemas/         # Pydantic models
│   │   ├── ai_prompts/      # Prompts para OpenAI
│   │   ├── utils/           # Utilitários (PDF parsing, etc)
│   │   └── core/            # Configuração
│   ├── tests/
│   └── requirements.txt
│
├── docker/
│   ├── docker-compose.yml   # Orquestração de serviços
│   ├── ai-service.Dockerfile
│   ├── backend.Dockerfile
│   ├── frontend.Dockerfile
│   └── init.sql             # SQL inicial (opcional)
│
├── .env                      # Variáveis de ambiente
├── .env.example             # Template do .env
└── README.md                # Este arquivo
```

---

## 🧪 Testes

### Backend (Spring Boot)
```bash
cd backend
mvn test
```

### Frontend (Angular)
```bash
cd frontend
ng test
```

### AI Service (Python)
```bash
cd ai-service
pytest tests/
pytest tests/ -v  # Verbose
```

---

## 🚢 Deploy

### Vercel (Frontend)

1. Conecte seu repositório GitHub ao Vercel
2. Defina Build Command: `npm run build`
3. Defina Output Directory: `dist/frontend/browser`
4. Configure variável de ambiente: `BACKEND_URL=https://seu-backend.com`

### Railway (Backend e AI Service)

1. Conecte repositório ao Railway
2. Crie um projeto para cada serviço (backend, ai-service)
3. Configure variáveis de ambiente (.env)
4. Defina o comando de build/start conforme Dockerfile

#### Arquivo railway.json (exemplo)
```json
{
  "build": {
    "builder": "dockerfile"
  },
  "deploy": {
    "restartPolicyType": "always",
    "restartPolicyMaxRetries": 10
  }
}
```

---

## 🔐 Segurança

### JWT Authentication
- Token gerado no login com validade configurável
- Enviado em header Authorization: `Bearer <token>`
- Validado em cada request
- Refresh token (implementação futura)

### Senhas
- Hash com BCrypt (backend)
- Validação de força (minúsculas, maiúsculas, números, símbolos)

### Dados Sensíveis
- `.env` nunca deve ser commitado (use `.env.example`)
- OpenAI API Key protegida no servidor
- HTTPS obrigatório em produção
- CORS configurado apenas para domínios permitidos

---

## 🐛 Troubleshooting

### Backend não conecta ao PostgreSQL
```bash
# Verificar logs do banco
docker compose logs postgres

# Verificar credenciais no .env
# Padrão: resume_user / resume_password
```

### AI Service retorna 0 no ATS score
- Verificar se OPENAI_API_KEY está correta no .env
- Verificar limite de API credits OpenAI
- Verificar logs: `docker compose logs ai-service`

### Frontend não consegue chamar backend
- Verificar se CORS está habilitado no backend
- Verificar URL do backend em `frontend/src/environments/`
- Testar: `curl http://localhost:8080/api/health`

### Docker não consegue buildar
```bash
# Limpar cache
docker compose down -v
docker system prune -a

# Rebuild
docker compose up --build
```

---

## 🤝 Contribuindo

1. Crie uma branch: `git checkout -b feature/sua-feature`
2. Commit suas mudanças: `git commit -m 'Add: sua feature'`
3. Push para branch: `git push origin feature/sua-feature`
4. Abra um Pull Request

---

## 📝 Licença

Este projeto é fornecido como-está para fins educacionais e comerciais.

---

## 📧 Suporte

Para issues, dúvidas ou sugestões, abra uma issue no repositório.

---

**Última atualização**: Abril 2026
