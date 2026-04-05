# ⚡ Guia Rápido de Testes - 5 Minutos

## 🎯 Opção Mais Rápida (Docker Compose)

### Terminal 1: Inicie tudo
```powershell
cd C:\Projects\Saas\docker
docker compose up --build
```

**Aguarde até ver**:
```
✅ postgres_1 ready to accept connections
✅ ai-service listening on 0.0.0.0:8000
✅ backend started on port 8080
✅ frontend running on port 4200
```

### Terminal 2: Teste os serviços
```powershell
cd C:\Projects\Saas
.\test-system.ps1

# Opção 6: Ver status
# Opção 3: Testar serviços
```

### Terminal 3: Abra o browser
```
http://localhost:4200
```

---

## ✅ Checklist de Teste (5 minutos)

### 1. Registrar (30 seg)
```
▶ Clique "Sign up"
▶ Email: test@example.com
▶ Senha: password123
▶ Confirme
✅ Deve redirecionar para Dashboard
```

### 2. Fazer Login (20 seg)
```
▶ Logout
▶ "Sign in"
▶ Email: test@example.com
▶ Senha: password123
✅ Deve aparecer dashboard
```

### 3. Analisar Resume (3 min)
```
▶ Job Description:
  "Senior Java Developer with Spring Boot, Docker, Kubernetes"

▶ Resume:
  "JOHN DOE - Senior Engineer
   Experience: Java, Spring Boot, Docker
   Education: BS Computer Science"

▶ Clique "Analyze & Optimize"

✅ Deve mostrar:
  • ATS Score (ex: 75/100)
  • Missing Keywords
  • Suggestions
  • Download button
```

### 4. Download (20 seg)
```
▶ Clique "Download"
✅ Arquivo "optimized-resume.txt" deve baixar
```

---

## 🐛 Se algo falhar...

### Porta ocupada
```powershell
# Descubra qual processo está usando
netstat -ano | findstr :8000
netstat -ano | findstr :8080
netstat -ano | findstr :4200
netstat -ano | findstr :5432

# Mate o processo
taskkill /PID <numero> /F
```

### Container não inicia
```powershell
# Reinicie tudo
docker compose down -v
docker compose up --build
```

### Módulos Python não instalam
```powershell
cd ai-service
pip install -r requirements.txt --upgrade
```

### Angular não funciona
```powershell
cd frontend
npm install
ng serve
```

---

## 📊 Comando Útil: Ver logs de um serviço específico

```powershell
# Ver logs da AI Service
docker compose logs ai-service

# Ver logs do Backend
docker compose logs backend

# Ver logs do Database
docker compose logs postgres

# Ver logs em tempo real
docker compose logs -f ai-service
```

---

## 🎓 Estrutura de Portas

| Serviço | Porta | URL |
|---------|-------|-----|
| Frontend | 4200 | http://localhost:4200 |
| Backend | 8080 | http://localhost:8080 |
| AI Service | 8000 | http://localhost:8000 |
| Database | 5432 | localhost:5432 |

---

## ✨ Esperado vs Real

### ✅ Login funciona
```
Quando clica em "Sign in":
▶ Formulário valida email
▶ Valida senha (min 6 chars)
▶ Envia POST para http://localhost:8080/auth/login
▶ JWT salvo em localStorage
▶ Redireciona para /dashboard
```

### ✅ Dashboard abre
```
Quando abre dashboard:
▶ Vê seu email na barra superior
▶ Pode colar Job Description
▶ Pode fazer upload de resume (PDF/DOCX)
▶ Ou colar texto do resume
```

### ✅ Análise funciona
```
Quando clica "Analyze & Optimize":
▶ Loading spinner aparece
▶ Backend chama AI Service
▶ Resultado aparece em "Results" tab
▶ ATS Score mostra cor (verde/amarelo/vermelho)
▶ Pode fazer download
```

---

## 🚀 Próximos passos após testes bem-sucedidos

1. **Explorar dados reais**
   - Use seu próprio resume
   - Use job descriptions reais do LinkedIn
   
2. **Monitorar performance**
   ```powershell
   docker stats
   ```
   
3. **Verificar logs**
   ```powershell
   docker compose logs | Select-String "error\|ERROR\|exception"
   ```

4. **Fazer commits**
   ```bash
   git add .
   git commit -m "Testing complete - system working"
   ```

---

## 🆘 Contato com Bugs

Se algo não funciona:

1. **Salve os logs**
   ```powershell
   docker compose logs > logs.txt
   ```

2. **Descreva o problema**
   - O que estava tentando fazer
   - Qual foi o erro
   - Cole os logs relevantes

3. **Tente resetar**
   ```powershell
   docker compose down -v
   docker compose up --build
   ```

---

**Tempo estimado de teste**: 5-10 minutos  
**Dificuldade**: Muito Fácil ✅  
**Resultado esperado**: Sistema completo funcionando 🎉

