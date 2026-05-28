# ✅ CHECKLIST - INTEGRAÇÃO BACKEND FRONTEND

## 📋 Antes de Começar
- [ ] Clonar/ter acesso ao repositório
- [ ] Python 3.8+ instalado
- [ ] pip instalado
- [ ] Virtual environment criado (recomendado)

## 🔧 Setup Backend

### Passo 1: Instalar Dependências
```bash
cd sistemaLogin
pip install -r requirements.txt
```
- [ ] Dependências instaladas sem erros

### Passo 2: Executar Setup Automático
```bash
python setup.py
```
- [ ] Migrações executadas
- [ ] Dados padrão criados
- [ ] Tabelas verificadas

**OU Passo 2 (Manual):**
```bash
python manage.py makemigrations instituicao
python manage.py makemigrations agenda
python manage.py migrate
```
- [ ] Migrações completadas
- [ ] Banco de dados atualizado

### Passo 3: Criar Superusuário
```bash
python manage.py createsuperuser
```
- [ ] Email: `admin@amores.com`
- [ ] Senha: (segura)
- [ ] Superusuário criado

### Passo 4: Iniciar o Servidor
```bash
python manage.py runserver
```
- [ ] Servidor rodando em `http://localhost:8000`

## 🧪 Testar API

### Endpoint: Informações da Instituição
```bash
curl http://localhost:8000/api/v1/instituicao/principal/
```
- [ ] Retorna dados em JSON
- [ ] Status 200 OK

### Endpoint: Criar Agendamento
```bash
curl -X POST http://localhost:8000/api/v1/agendamentos/api/ \
  -H "Content-Type: application/json" \
  -d '{"nome":"João","data_visita":"2026-05-20","horario_preferencial":"09:00:00"}'
```
- [ ] Retorna status 201 Created
- [ ] Agendamento salvo no banco

### Endpoint: Listar Agendamentos
```bash
curl http://localhost:8000/api/v1/agendamentos/api/listar/
```
- [ ] Retorna lista de agendamentos
- [ ] Status 200 OK

## 🖥️ Acessar Painel Admin

1. Abra: `http://localhost:8000/admin/`
2. Login com credenciais criadas
- [ ] Acesso ao admin
- [ ] Seção "Instituições" visível
- [ ] Seção "Agendamentos" visível

## 📚 Documentação da API

### Swagger UI
```
http://localhost:8000/api/schema/swagger-ui/
```
- [ ] Documentação visual disponível

### ReDoc
```
http://localhost:8000/api/schema/redoc/
```
- [ ] Documentação alternativa disponível

## 🌐 Frontend Integration

### Se usando HTML/JavaScript:
- [ ] Copiar `api-integration-example.js` para `front/`
- [ ] Atualizar `front/script.js` com as funções da API
- [ ] Testar no navegador (F12 > Console)

### Se usando React/Vue:
- [ ] Usar fetch/axios para chamadas HTTP
- [ ] Referência: `front/api-integration-example.js`

## 📋 Verificação Final

### Estrutura
- [ ] Pasta `apps/instituicao/` existe
- [ ] Pasta `agenda/` tem `serializers.py`
- [ ] `sistemaLogin/settings.py` contém `'apps.instituicao'`
- [ ] `sistemaLogin/urls.py` contém rota de instituição

### Banco de Dados
- [ ] Tabela `apps_instituicao_instituicao` criada
- [ ] Tabela `agenda_agendamento` atualizada
- [ ] Um registro padrão de `Instituição` existe

### API
- [ ] GET `/api/v1/instituicao/principal/` ✅
- [ ] POST `/api/v1/agendamentos/api/` ✅
- [ ] GET `/api/v1/agendamentos/api/listar/` ✅

## 🚀 Deploy (Futuro)

- [ ] Coletar statics: `python manage.py collectstatic`
- [ ] Configurar variáveis de ambiente
- [ ] Usar production server (gunicorn)
- [ ] Configurar CORS para domínio de produção

## 📞 Troubleshooting

### Problema: ModuleNotFoundError para instituicao
**Solução:**
```bash
python manage.py startapp instituicao apps
# Copiar arquivos manualmente
```

### Problema: Tabelas não encontradas
**Solução:**
```bash
python manage.py migrate --run-syncdb
```

### Problema: CORS error no frontend
**Solução:**
1. Verificar `CORS_ALLOWED_ORIGINS` em settings.py
2. Reiniciar servidor Django
3. Limpar cache do navegador

### Problema: Porta 8000 já em uso
**Solução:**
```bash
python manage.py runserver 8001
```

## 📝 Notas

- Backend segue padrão REST API
- Dados da instituição podem ser editados no admin
- Agendamentos são salvos automaticamente
- CORS já está configurado para local testing
- Documentação completa em `API_DOCS.md`

## ✨ Próximas Etapas

1. [ ] Integrar frontend com API JavaScript
2. [ ] Adicionar validações extras
3. [ ] Implementar autenticação JWT
4. [ ] Setup de produção
5. [ ] CI/CD pipeline

---

**Criado em:** 2026-05-16  
**Status:** ✅ Backend Adaptado e Pronto para Uso
