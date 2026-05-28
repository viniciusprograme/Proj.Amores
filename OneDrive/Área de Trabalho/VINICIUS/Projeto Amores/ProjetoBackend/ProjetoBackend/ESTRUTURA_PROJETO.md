# 📁 Estrutura do Projeto - Market Solutions Platform

## 🎯 Visão Geral

Este é um **backend de API RESTful** para gerenciar usuários, autenticação e produtos. O projeto é organizado de forma modular, seguindo as melhores práticas de Django.

---

## 📂 Árvore Completa da Pasta

```
ProjetoBackend/
│
├── 📁 sistemaLogin/              [Raiz do Projeto Django]
│   ├── 📁 apps/                  [Aplicações Principais]
│   │   ├── 📁 users/             [Gestão de Usuários]
│   │   │   ├── models.py         [Modelo User com email]
│   │   │   ├── views.py          [Endpoints de autenticação]
│   │   │   ├── serializers.py    [Validação de dados]
│   │   │   ├── urls.py           [Rotas do app users]
│   │   │   ├── apps.py           [Configuração do app]
│   │   │   └── migrations/       [Histórico de banco]
│   │   │
│   │   ├── 📁 products/          [Gestão de Produtos]
│   │   │   ├── models.py         [Models Product, Category]
│   │   │   ├── views.py          [Endpoints de produtos]
│   │   │   ├── serializers.py    [Validação de dados]
│   │   │   ├── urls.py           [Rotas do app products]
│   │   │   ├── apps.py           [Configuração do app]
│   │   │   └── migrations/       [Histórico de banco]
│   │   │
│   │   ├── 📁 authentication/    [Autenticação (auxiliar)]
│   │   │   ├── apps.py
│   │   │   ├── urls.py
│   │   │   └── __init__.py
│   │   │
│   │   └── 📁 common/            [Utilitários Comuns]
│   │       ├── apps.py
│   │       ├── urls.py
│   │       └── __init__.py
│   │
│   ├── 📁 core/                  [Configuração Central]
│   │   ├── middleware.py         [JWT Middleware]
│   │   ├── apps.py               [Configuração core]
│   │   └── __init__.py
│   │
│   ├── 📁 formulario/            [App Legado (Web)]
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── templates/            [HTML Templates]
│   │
│   ├── 📁 sistemaLogin/          [Configurações Django]
│   │   ├── settings.py           [Variáveis do Django]
│   │   ├── urls.py               [Roteamento Principal]
│   │   ├── wsgi.py               [Interface Web]
│   │   ├── asgi.py               [Interface Async]
│   │   └── templates/            [Templates Base]
│   │
│   ├── 📁 logs/                  [Arquivos de Log]
│   ├── 📁 migrations/            [Migrações Gerais]
│   ├── db.sqlite3                [Banco de Dados SQLite]
│   └── manage.py                 [Gerenciador Django]
│
├── 📁 core/                      [Core API (antiga estrutura)]
│   ├── middleware.py
│   └── __init__.py
│
├── 📁 docker/                    [Arquivos Docker]
│   └── (possíveis configs)
│
├── 📁 scripts/                   [Scripts Utilitários]
│   ├── init.sh                   [Script de inicialização]
│
├── 📁 tests/                     [Testes Automatizados]
│   └── (testes dos apps)
│
├── 📁 database/                  [Dados do Banco]
│
├── 📁 agenda/                    [App Legado (Agendamentos)]
│
├── Dockerfile                    [Configuração Docker]
├── docker-compose.yml            [Orquestração Docker]
├── requirements.txt              [Dependências Python]
├── nginx.conf                    [Configuração Nginx]
├── pytest.ini                    [Config Testes]
├── README.md                     [Documentação Principal]
├── .env                          [Variáveis de Ambiente]
│
└── 📁 ../ (raiz externa)
    ├── .venv/                    [Ambiente Virtual]
    ├── .git/                     [Controle de Versão]
    └── ...

```

---

## 🔍 Explicação Detalhada de Cada Pasta

### 📁 **sistemaLogin/** - Raiz do Projeto Django
O diretório principal do projeto. Contém todas as aplicações, configurações e banco de dados.

---

### 📁 **sistemaLogin/apps/** - Aplicações Principais
Aqui estão todos os módulos funcionais do sistema, organizados por responsabilidade.

#### 📁 **apps/users/** - Gestão de Usuários e Autenticação
**O que faz:**
- Gerencia login, registro e autenticação de usuários
- Implementa modelo de usuário customizado (usa email em vez de username)
- Gera tokens JWT para autenticação

**Arquivos principais:**
- `models.py` - Define o modelo `User` com campos customizados
- `views.py` - Endpoints para login, registro, refresh de token
- `serializers.py` - Valida e transforma dados de entrada
- `urls.py` - Rotas como `/api/v1/users/auth/login/`

**Funcionalidade chave:**
```
Email-based login (sem username)
JWT authentication (tokens de segurança)
Perfil de usuário com avatar, bio, telefone
```

---

#### 📁 **apps/products/** - Gestão de Produtos e Categorias
**O que faz:**
- Gerencia catálogo de produtos
- Organiza produtos em categorias
- Disponibiliza busca e filtros

**Arquivos principais:**
- `models.py` - Define `Product` e `Category`
- `views.py` - Endpoints de produtos e categorias
- `serializers.py` - Transforma dados de produtos
- `urls.py` - Rotas como `/api/v1/products/public/featured/`

**Funcionalidade chave:**
```
CRUD de produtos (criar, ler, atualizar, deletar)
Categorias de produtos
Produtos em destaque (featured)
Busca de produtos por termo
Preços, descontos, estoque
```

---

#### 📁 **apps/authentication/** - Autenticação Auxiliar
App auxiliar para lógica adicional de autenticação se necessário.

---

#### 📁 **apps/common/** - Utilitários Comuns
App para funcionalidades compartilhadas entre outras apps.

---

### 📁 **sistemaLogin/core/** - Middleware e Configurações Centrais

**O que faz:**
- Middleware JWT para validar tokens automaticamente
- Integração central de segurança

**Arquivo importante:**
- `middleware.py` - Valida JWT tokens nas requisições (autenticação opcional)

---

### 📁 **sistemaLogin/sistemaLogin/** - Configurações Django

**O que faz:**
- Centraliza todas as configurações do Django

**Arquivos principais:**
- `settings.py` - **Arquivo mais importante!** Define:
  - Banco de dados
  - Apps instalados
  - Middleware
  - Autenticação JWT
  - CORS (permite requisições de outros domínios)
  - Documentação da API
  
- `urls.py` - Rota principal, direciona para endpoints da API

- `wsgi.py` - Interface para servir a aplicação (produção)

- `asgi.py` - Interface assíncrona

---

### 📁 **sistemaLogin/formulario/** - App Legado (Web)
Antiga interface web do projeto. Pode ser ignorada na maioria dos casos.

---

### 📁 **docker/** - Containerização
Arquivos para rodarcomo container Docker.

---

### 📁 **scripts/** - Scripts Úteis
Scripts para automatizar tarefas comuns.

**Arquivo importante:**
- `init.sh` - Inicializa o projeto (cria migrations, cria admin, etc.)

---

### 📁 **tests/** - Testes Automatizados
Testes para garantir que o código funciona corretamente.

---

## 🔄 Fluxo de Funcionamento

```
1. Usuário faz requisição HTTP
   ↓
2. Django recebe na URL (urls.py)
   ↓
3. Middleware JWT valida o token (se necessário)
   ↓
4. View processa a requisição
   ↓
5. Serializer valida e transforma dados
   ↓
6. Model interage com banco de dados
   ↓
7. Resposta JSON é enviada ao usuário
```

---

## 📊 Responsabilidades por Arquivo

| Arquivo | Responsabilidade |
|---------|------------------|
| `models.py` | Define estrutura de dados no banco |
| `views.py` | Lógica dos endpoints da API |
| `serializers.py` | Valida e transforma dados |
| `urls.py` | Define rotas e endpoints |
| `settings.py` | Configuração central Django |
| `middleware.py` | Intercepta requisições para segurança |
| `apps.py` | Configuração da aplicação |

---

## 🔐 Partes de Segurança

- **`core/middleware.py`** - Valida tokens JWT
- **`settings.py`** - Configurações de segurança Django
- **`.env`** - Variáveis secretas (não versionadas)
- **JWT Tokens** - Autenticação estateless

---

## 🗄️ Partes de Banco de Dados

- **`db.sqlite3`** - Arquivo do banco (desevolvimento)
- **`apps/users/migrations/`** - Histórico de mudanças de User
- **`apps/products/migrations/`** - Histórico de mudanças de Products

---

## 🐳 Partes de Docker

- **`Dockerfile`** - Receita para criar container
- **`docker-compose.yml`** - Orquestra múltiplos containers
- **`nginx.conf`** - Configuração do servidor web reverso

---

## 🔌 Partes de API

- **`apps/users/views.py`** - Endpoints de usuários
- **`apps/products/views.py`** - Endpoints de produtos
- **`sistemaLogin/urls.py`** - Rota principal (`/api/v1/`)

---

## 📚 Backend vs Frontend

### Backend (Este projeto)
- ✅ Gerencia dados
- ✅ Autenticação e segurança
- ✅ Validação
- ✅ Banco de dados

### Frontend (Não está aqui)
- Seria feito com React, Vue ou Angular
- Faz requisições para este backend
- Exibe dados ao usuário

---

## 🚀 Como o Projeto Inicia

```bash
python manage.py migrate      # Cria tabelas no banco
python manage.py runserver    # Inicia o servidor
```

Após iniciar:
- API disponível em: `http://localhost:8000/api/v1/`
- Documentação: `http://localhost:8000/api/schema/swagger-ui/`
- Admin: `http://localhost:8000/admin/`

---

## ✅ Checklist de Entendimento

- [ ] Entendi que **users** gerencia login
- [ ] Entendi que **products** gerencia catálogo
- [ ] Entendi que **core** tem middleware de segurança
- [ ] Entendi que **sistemaLogin** é a configuração central
- [ ] Entendi que **models.py** define dados
- [ ] Entendi que **views.py** define endpoints
- [ ] Entendi que **urls.py** mapeia rotas
- [ ] Entendi que **serializers.py** valida dados

---

**Criado para facilitar o onboarding de novos membros da equipe! 🎓**
