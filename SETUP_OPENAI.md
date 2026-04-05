# 🔑 Configuração da Chave OpenAI

## ⚠️ IMPORTANTE: Seu Sistema Está em Modo Mock

Você recebeu a mensagem:
```
Set OPENAI_API_KEY environment variable for real AI-powered analysis.
```

Isso significa que **nenhuma chave OpenAI foi encontrada** e o sistema está usando respostas simuladas (mock).

---

## 🚀 Como Configurar

### Opção 1: Configuração Rápida (Recomendado)

#### Passo 1: Obter sua Chave OpenAI
1. Acesse https://platform.openai.com/api-keys
2. Faça login com sua conta OpenAI (crie uma se não tiver)
3. Clique em "Create new secret key"
4. Copie a chave (ela começa com `sk-proj-`)

#### Passo 2: Adicionar ao .env
```bash
# Abra o arquivo .env
notepad C:\Projects\Saas\.env
```

**Encontre esta linha:**
```env
OPENAI_API_KEY=your-openai-api-key-here
```

**Substitua por sua chave:**
```env
OPENAI_API_KEY=sk-proj-sua-chave-aqui
```

**IMPORTANTE:** Não cometa esta chave! Ela permanece apenas em `.env` (que está no `.gitignore`)

#### Passo 3: Reiniciar os Containers
```powershell
cd C:\Projects\Saas\docker
docker-compose down
docker-compose up -d
```

Aguarde ~2 minutos até todos os containers estarem saudáveis:
```powershell
docker-compose ps
```

---

## ✅ Verificar se Está Funcionando

### Teste 1: Verificar se a Chave Foi Carregada
```powershell
docker exec resume-optimizer-ai python -c "from app.core.config import settings; print(f'API Key Set: {bool(settings.openai_api_key)}'); print(f'First 10 chars: {settings.openai_api_key[:10] if settings.openai_api_key else \"NOT SET\"}')"
```

Esperado: `API Key Set: True` e `First 10 chars: sk-proj-...`

### Teste 2: Testar ATS Score Real
```powershell
cd C:\Projects\Saas

$body = @{
    job_description = "Python Developer with 5 years experience, Django, PostgreSQL, Redis"
    resume_text = "Python developer with 7 years of experience. Expertise in Django, PostgreSQL, and Redis. Led team of 3 developers."
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:8080/api/resumes/analyze" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer YOUR_TOKEN"} `
    -Body $body `
    -UseBasicParsing

$response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

### Teste 3: Verificar Logs
```powershell
docker logs resume-optimizer-ai --tail 50
```

Procure por:
- ✅ `ChatOpenAI initialized` = Funcionando com AI Real
- ❌ `No OPENAI_API_KEY found` = Ainda em modo mock

---

## 🛠️ Resolução de Problemas

### Problema 1: "API Key Set: False"
**Causa:** A chave não foi carregada corretamente

**Solução:**
1. Verifique o arquivo `.env` tem a chave correta
2. Certifique-se que NÃO há espaços extras
3. Reinicie os containers: `docker-compose restart ai-service`

### Problema 2: "Invalid API Key"
**Causa:** A chave é inválida ou expirou

**Solução:**
1. Gere uma nova chave em https://platform.openai.com/api-keys
2. Atualize o arquivo `.env`
3. Reinicie os containers

### Problema 3: "Quota exceeded"
**Causa:** Sua conta OpenAI não tem créditos

**Solução:**
1. Acesse https://platform.openai.com/account/billing/overview
2. Adicione método de pagamento
3. Verifique saldo em "Usage"

### Problema 4: "Connection timeout"
**Causa:** Firewall ou proxy bloqueando conexão com OpenAI

**Solução:**
1. Verifique se consegue acessar https://api.openai.com
2. Configure proxy se necessário
3. Verifique regras de firewall

---

## 📝 Como Funciona Agora

### Modo MOCK (sem chave OpenAI)
- ❌ ATS Score: Retorna valores genéricos
- ❌ Optimized Resume: Retorna o mesmo input
- ❌ Suggestions: Retorna sugestões pré-definidas

### Modo REAL (com chave OpenAI válida)
- ✅ ATS Score: Análise IA real baseada em keywords
- ✅ Optimized Resume: Reescreve resume com melhorias reais
- ✅ Suggestions: Gera sugestões personalizadas
- ✅ Performance: Mais lento (chamadas à API)
- 💰 Custo: ~$0.001 por análise (gpt-4o-mini)

---

## 🔒 Segurança

### ✅ Boas Práticas
1. **Nunca comita a chave** - já está no `.gitignore`
2. **Use variáveis de ambiente** - em produção
3. **Regenere a chave** - se vazar
4. **Monitore uso** - em https://platform.openai.com/account/billing/usage

### ⚠️ Para Produção
```bash
# Use gerenciador de secrets
# AWS Secrets Manager
# GitHub Secrets
# HashiCorp Vault
# Railway Environment Variables
```

---

## 📞 Suporte

Se problemas persistirem:
1. Verifique logs: `docker logs resume-optimizer-ai`
2. Teste a chave: https://platform.openai.com/account/api-keys
3. Verifique créditos: https://platform.openai.com/account/billing/usage

---

**Status Atual:** Sistema em Modo Mock (sem chave OpenAI)  
**Próximo Passo:** Configure sua chave OpenAI acima

