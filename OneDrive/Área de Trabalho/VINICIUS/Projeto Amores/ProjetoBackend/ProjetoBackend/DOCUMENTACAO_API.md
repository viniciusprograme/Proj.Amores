# 🚀 Documentação da API - Market Solutions Platform

## 📋 Índice
1. [Visão Geral](#visão-geral)
2. [Configuração](#configuração)
3. [Rotas da API](#rotas-da-api)
4. [Autenticação](#autenticação)
5. [Segurança](#segurança)
6. [Banco de Dados](#banco-de-dados)
7. [Docker](#docker)
8. [Estrutura Técnica](#estrutura-técnica)
9. [Troubleshooting](#troubleshooting)

---

##  Visão Geral

### O que é?
Este é um **backend de API RESTful** completo para um sistema de gerenciamento de usuários e produtos.

### Objetivo
Fornecer endpoints para:
-  Registrar e autenticar usuários
-  Gerenciar perfil do usuário
-  Listar e buscar produtos
-  Gerenciar categorias
-  Controle de acesso com JWT

### Tecnologias Principais
```
Django 6.0.5          - Framework web
Django REST Framework - API RESTful
Simple JWT            - Autenticação com tokens
SQLite3               - Banco de dados (desenvolvimento)
Docker                - Containerização
PostgreSQL Ready      - Para produção
```

### Versão da API
```
v1 - Versão atual
http://localhost:8000/api/v1/
```

---

##  Configuração

### 1. Pré-requisitos
```
Python 3.8+
pip (gerenciador de pacotes)
Git (controle de versão)
```

### 2. Instalação Passo a Passo

#### Passo 1: Clonar/Navegar para o projeto
```bash
cd ProjetoBackend/sistemaLogin
```

#### Passo 2: Criar ambiente virtual (se não existir)
```bash
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate

# Ativar (Linux/Mac)
source venv/bin/activate
```

#### Passo 3: Instalar dependências
```bash
pip install -r requirements.txt
```

#### Passo 4: Criar arquivo .env
Crie `ProjetoBackend/.env`:
```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7

DATABASE_URL=sqlite:///db.sqlite3
```

#### Passo 5: Executar Migrações
```bash
python manage.py migrate
```

#### Passo 6: Criar Superusuário (Admin)
```bash
python manage.py shell -c "from apps.users.models import User; User.objects.create_superuser('admin@marketsolutions.com', 'Admin123!', first_name='Admin', last_name='User')"
```

#### Passo 7: Iniciar Servidor
```bash
python manage.py runserver
```

**Servidor rodando em:** `http://localhost:8000`

---

##  Rotas da API

###  Base URL
```
http://localhost:8000/api/v1/
```

###  AUTENTICAÇÃO - Endpoints de Login/Registro

#### 1. Registrar Novo Usuário
```
POST /api/v1/users/auth/register/
```

**Autenticação:** Não requerida

**Body (JSON):**
```json
{
  "email": "novo@example.com",
  "first_name": "João",
  "last_name": "Silva",
  "password": "SenhaSegura123!",
  "password_confirm": "SenhaSegura123!"
}
```

**Resposta (201 - Sucesso):**
```json
{
  "user": {
    "id": 1,
    "email": "novo@example.com",
    "first_name": "João",
    "last_name": "Silva",
    "is_profile_complete": false,
    "profile_completion_percentage": 50
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

**Status de Erro (400):**
```json
{
  "email": ["user with this email already exists"]
}
```

---

#### 2. Fazer Login
```
POST /api/v1/users/auth/login/
```

**Autenticação:** Não requerida

**Body (JSON):**
```json
{
  "email": "admin@marketsolutions.com",
  "password": "Admin123!"
}
```

**Resposta (200 - Sucesso):**
```json
{
  "user": {
    "id": 1,
    "email": "admin@marketsolutions.com",
    "first_name": "Admin",
    "last_name": "User",
    "is_profile_complete": true,
    "profile_completion_percentage": 100
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

**Status de Erro (401):**
```json
{
  "error": "Invalid credentials"
}
```

**Como usar:**
1. Guarde o `access` token
2. Use-o no header `Authorization: Bearer {access_token}` nas próximas requisições

---

#### 3. Obter Perfil Atual
```
GET /api/v1/users/me/
```

**Autenticação:**  Obrigatória (JWT Token)

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Resposta (200 - Sucesso):**
```json
{
  "id": 1,
  "email": "admin@marketsolutions.com",
  "first_name": "Admin",
  "last_name": "User",
  "phone_number": "+55 11 99999-9999",
  "bio": "Sou um admin",
  "avatar": "https://example.com/avatar.jpg",
  "date_of_birth": "1990-01-15",
  "is_profile_complete": true,
  "profile_completion_percentage": 100,
  "is_active": true,
  "date_joined": "2026-05-13T10:00:00Z"
}
```

---

#### 4. Atualizar Perfil
```
PATCH /api/v1/users/update_profile/
```

**Autenticação:**  Obrigatória

**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "first_name": "João",
  "phone_number": "+55 11 98888-8888",
  "bio": "Novo bio"
}
```

**Resposta (200 - Sucesso):**
```json
{
  "first_name": "João",
  "last_name": "User",
  "phone_number": "+55 11 98888-8888",
  "bio": "Novo bio",
  "profile_completion_percentage": 100
}
```

---

#### 5. Renovar Token de Acesso
```
POST /api/v1/users/auth/token_refresh/
```

**Autenticação:**  Obrigatória

**Body (JSON):**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Resposta (200 - Sucesso):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Uso:** Quando o token de acesso expira, use o token de refresh para obter um novo

---

### 📦 PRODUTOS - Endpoints de Produtos

#### 1. Listar Produtos em Destaque (Público)
```
GET /api/v1/products/public/featured/
```

**Autenticação:**  Não requerida

**Query Parameters:**
```
(nenhum)
```

**Resposta (200 - Sucesso):**
```json
[
  {
    "id": 1,
    "name": "Smartphone XYZ",
    "description": "Um smartphone incrível com câmera de 50MP",
    "price": "1999.99",
    "discount_percentage": "10.00",
    "discounted_price": "1799.99",
    "stock_quantity": 50,
    "category_name": "Eletrônicos",
    "is_featured": true,
    "slug": "smartphone-xyz"
  }
]
```

---

#### 2. Buscar Produtos (Público)
```
GET /api/v1/products/public/search/?q=termo
```

**Autenticação:**  Não requerida

**Query Parameters:**
```
q = termo de busca (nome, descrição ou SKU)
```

**Exemplo:**
```
GET /api/v1/products/public/search/?q=smartphone
```

**Resposta (200 - Sucesso):**
```json
[
  {
    "id": 1,
    "name": "Smartphone XYZ",
    "description": "Um smartphone incrível com câmera de 50MP",
    "price": "1999.99",
    "discounted_price": "1799.99",
    "stock_quantity": 50,
    "category_name": "Eletrônicos",
    "slug": "smartphone-xyz"
  }
]
```

---

#### 3. Listar Categorias (Autenticado)
```
GET /api/v1/products/categories/
```

**Autenticação:**  Obrigatória

**Headers:**
```
Authorization: Bearer {token}
```

**Query Parameters (Opcionais):**
```
search = buscar por nome
ordering = ordenar por: name, order, created_at
```

**Resposta (200 - Sucesso):**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Eletrônicos",
      "description": "Produtos eletrônicos e gadgets",
      "slug": "eletronicos",
      "image": null,
      "is_active": true,
      "order": 0,
      "created_at": "2026-05-13T10:00:00Z"
    }
  ]
}
```

---

#### 4. Criar Categoria (Admin)
```
POST /api/v1/products/categories/
```

**Autenticação:**  Obrigatória (Admin apenas)

**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "name": "Eletrônicos",
  "description": "Produtos eletrônicos e gadgets",
  "slug": "eletronicos"
}
```

**Resposta (201 - Criado):**
```json
{
  "id": 1,
  "name": "Eletrônicos",
  "description": "Produtos eletrônicos e gadgets",
  "slug": "eletronicos",
  "is_active": true,
  "order": 0,
  "created_at": "2026-05-13T10:00:00Z"
}
```

---

#### 5. Listar Todos os Produtos (Autenticado)
```
GET /api/v1/products/products/
```

**Autenticação:**  Obrigatória

**Headers:**
```
Authorization: Bearer {token}
```

**Query Parameters (Opcionais):**
```
status = draft, active, inactive, discontinued
category = id da categoria
is_featured = true/false
search = buscar por nome, descrição ou SKU
ordering = price, -price (decrescente), created_at, -created_at
```

**Resposta (200 - Sucesso):**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Smartphone XYZ",
      "description": "Um smartphone incrível com câmera de 50MP",
      "price": "1999.99",
      "cost_price": "1500.00",
      "discount_percentage": "10.00",
      "discounted_price": "1799.99",
      "stock_quantity": 50,
      "min_stock_level": 10,
      "sku": "PRD-ABC12345",
      "category": 1,
      "category_name": "Eletrônicos",
      "status": "active",
      "is_featured": true,
      "is_available": true,
      "slug": "smartphone-xyz",
      "stock_status": "in_stock",
      "profit_margin": 24.88,
      "created_at": "2026-05-13T10:00:00Z"
    }
  ]
}
```

---

#### 6. Criar Produto (Admin)
```
POST /api/v1/products/products/
```

**Autenticação:**  Obrigatória (Admin apenas)

**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "name": "Smartphone XYZ",
  "description": "Um smartphone incrível com câmera de 50MP",
  "price": 1999.99,
  "cost_price": 1500.00,
  "discount_percentage": 10,
  "stock_quantity": 50,
  "min_stock_level": 10,
  "category": 1,
  "status": "active",
  "is_featured": true
}
```

**Resposta (201 - Criado):**
```json
{
  "id": 1,
  "name": "Smartphone XYZ",
  "price": "1999.99",
  "sku": "PRD-ABC12345",
  "stock_status": "in_stock",
  "created_at": "2026-05-13T10:00:00Z"
}
```

---

#### 7. Atualizar Estoque do Produto
```
PATCH /api/v1/products/products/{id}/update_stock/
```

**Autenticação:**  Obrigatória

**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "stock_quantity": 100
}
```

**Resposta (200 - Sucesso):**
```json
{
  "id": 1,
  "name": "Smartphone XYZ",
  "stock_quantity": 100,
  "stock_status": "in_stock"
}
```

---

###  ADMIN - Endpoints Administrativos

#### 1. Listar Todos os Usuários (Admin)
```
GET /api/v1/users/admin/users/
```

**Autenticação:**  Obrigatória (Admin apenas)

**Headers:**
```
Authorization: Bearer {token}
```

**Query Parameters (Opcionais):**
```
email = filtrar por email (busca parcial)
is_active = true/false
```

**Resposta (200 - Sucesso):**
```json
[
  {
    "id": 1,
    "email": "admin@marketsolutions.com",
    "first_name": "Admin",
    "last_name": "User",
    "is_active": true,
    "date_joined": "2026-05-13T10:00:00Z"
  },
  {
    "id": 2,
    "email": "usuario@example.com",
    "first_name": "João",
    "last_name": "Silva",
    "is_active": true,
    "date_joined": "2026-05-13T11:00:00Z"
  }
]
```

---

##  Autenticação

### Tipos de Autenticação

#### 1. JWT (JSON Web Token)
- **O que é:** Token seguro que valida a identidade do usuário
- **Como funciona:** Usuário faz login, recebe um token, usa o token em requisições futuras
- **Duração:** 
  - Access token: 60 minutos (configurável)
  - Refresh token: 7 dias (configurável)

#### 2. Como Usar Token

**Passo 1: Fazer Login**
```bash
curl -X POST http://localhost:8000/api/v1/users/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@marketsolutions.com",
    "password": "Admin123!"
  }'
```

**Passo 2: Guardar o `access` token recebido**
```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Passo 3: Usar o token em requisições**
```bash
curl -X GET http://localhost:8000/api/v1/users/me/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

#### 3. Token Expirado?
Quando o access token expira (após 60 min), use o refresh token:
```bash
curl -X POST http://localhost:8000/api/v1/users/auth/token_refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "seu_refresh_token_aqui"
  }'
```

---

## 🛡️ Segurança

### 1. Variáveis de Ambiente (.env)

**Arquivo:** `ProjetoBackend/.env`

```env
# NÃO DEIXE ISSO NO GIT!
SECRET_KEY=sua-chave-super-secreta-aqui

# Em desenvolvimento
DEBUG=True

# Em produção
DEBUG=False

# Hosts permitidos
ALLOWED_HOSTS=localhost,127.0.0.1,seu-dominio.com

# Configurações JWT
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
```

### 2. CORS (Cross-Origin Resource Sharing)

**O que é:** Permite que frontend em outro domínio acesse a API

**Configurado em:** `settings.py`

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Frontend React/Vue
    "https://seu-site.com",
]
```

### 3. Permissões

- **Público:** Rotas com `/public/` não precisam de autenticação
- **Autenticado:** Requer token JWT válido
- **Admin:** Requer permissão de administrador

### 4. Proteção Básica

-  Senhas com hash (não armazenadas em texto plano)
-  CSRF token para formulários
-  Rate limiting (controla requisições excessivas)
-  SQL injection protegida (ORM Django)
-  XSS protegida
-  Validação de entrada em todos os endpoints

---

##  Banco de Dados

### Tipo
```
SQLite3 (Desenvolvimento)
PostgreSQL (Produção)
```

### Arquivo
```
ProjetoBackend/sistemaLogin/db.sqlite3
```

### Principais Tabelas (Models)

#### 1. User (Usuários)
```
id              INT (PK)
email           VARCHAR (unique)
first_name      VARCHAR
last_name       VARCHAR
password        VARCHAR (hash)
phone_number    VARCHAR
avatar          ImageField
bio             TEXT
date_of_birth   DATE
is_staff        BOOLEAN
is_superuser    BOOLEAN
is_active       BOOLEAN
created_at      DATETIME
updated_at      DATETIME
```

#### 2. Category (Categorias)
```
id              INT (PK)
name            VARCHAR (unique)
description     TEXT
slug            VARCHAR (unique)
image           ImageField
is_active       BOOLEAN
order           INT
created_by      INT (FK → User)
created_at      DATETIME
updated_at      DATETIME
```

#### 3. Product (Produtos)
```
id                  INT (PK)
name                VARCHAR
description         TEXT
short_description   VARCHAR
price               DECIMAL
cost_price          DECIMAL
discount_percentage DECIMAL
stock_quantity      INT
min_stock_level     INT
sku                 VARCHAR (unique)
category            INT (FK → Category)
status              VARCHAR (draft/active/inactive/discontinued)
is_featured         BOOLEAN
is_available        BOOLEAN
main_image          ImageField
slug                VARCHAR (unique)
meta_title          VARCHAR
meta_description    VARCHAR
created_by          INT (FK → User)
created_at          DATETIME
updated_at          DATETIME
```

### Migrations

**O que é:** Histórico de alterações no banco de dados

**Arquivos:** `apps/users/migrations/`, `apps/products/migrations/`

**Comandos:**
```bash
# Ver status
python manage.py showmigrations

# Criar nova migração (depois de alterar models.py)
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Desfazer migração
python manage.py migrate app_name zero
```

---

##  Docker

### O que é?
Container que encapsula toda a aplicação em um ambiente isolado.

### Arquivos

#### Dockerfile
```dockerfile
FROM python:3.11-slim          # Imagem base
WORKDIR /app                   # Diretório de trabalho
COPY requirements.txt .        # Copia dependências
RUN pip install -r requirements.txt  # Instala dependências
COPY . .                       # Copia código
EXPOSE 8000                    # Expõe porta
CMD ["gunicorn", ...]          # Comando de inicialização
```

#### docker-compose.yml
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=True
    volumes:
      - .:/app
    command: python manage.py runserver 0.0.0.0:8000
```

### Como Usar

**Construir imagem:**
```bash
docker build -t market-solutions .
```

**Rodar container:**
```bash
docker-compose up
```

**Rodar em background:**
```bash
docker-compose up -d
```

**Parar container:**
```bash
docker-compose down
```

### Acessar dentro do Container
```bash
docker-compose exec web python manage.py shell
docker-compose exec web python manage.py migrate
```

---

##  Estrutura Técnica

### Arquitetura de Camadas

```
┌─────────────────────────────────┐
│   Requisição HTTP               │
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│   URLs (urls.py)                │ ← Roteia a requisição
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│   Middleware (middleware.py)    │ ← Valida JWT, CORS, etc
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│   Views (views.py)              │ ← Processa lógica
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│   Serializers (serializers.py)  │ ← Valida dados
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│   Models (models.py)            │ ← Interage com BD
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│   Banco de Dados (db.sqlite3)   │ ← Armazena dados
└─────────────────────────────────┘
             ↓
         [Resposta JSON volta]
```

### Padrão MVT (Model-View-Template)

- **Model:** Define dados (users, products)
- **View:** Lógica de negócio (processar requisição)
- **Template:** Retorna resposta (JSON para API)

### Padrão DRF (Django REST Framework)

- **Serializers:** Valida e transforma dados
- **ViewSets:** Agrupa operações (CRUD)
- **Routers:** Gera rotas automaticamente

---

## ❓ Troubleshooting

### Problema: "ModuleNotFoundError"
**Solução:** Ativar ambiente virtual
```bash
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### Problema: "No such table"
**Solução:** Executar migrações
```bash
python manage.py migrate
```

### Problema: "Invalid credentials"
**Solução:** Verificar email e senha
```
Email: admin@marketsolutions.com
Senha: Admin123!
```

### Problema: Porta 8000 já em uso
**Solução:** Usar outra porta
```bash
python manage.py runserver 8001
```

### Problema: JWT token expirado
**Solução:** Renovar token
```bash
POST /api/v1/users/auth/token_refresh/
{
  "refresh": "seu_refresh_token"
}
```

### Problema: CORS error no frontend
**Solução:** Configurar CORS em settings.py
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
```

---

##  Recursos Adicionais

### Documentação Automática
- **Swagger UI:** `http://localhost:8000/api/schema/swagger-ui/`
- **ReDoc:** `http://localhost:8000/api/schema/redoc/`
- **Schema JSON:** `http://localhost:8000/api/schema/`

### Postman Collection
- Arquivo: `ProjetoBackend/MarketSolutionsAPI.postman_collection.json`
- Importar no Postman para testar todos os endpoints

### Admin Panel
- URL: `http://localhost:8000/admin/`
- Email: `admin@marketsolutions.com`
- Senha: `Admin123!`

---

##  Checklist de Compreensão

- [ ] Consigo fazer login na API
- [ ] Consigo obter meu perfil com JWT
- [ ] Consigo buscar produtos públicos
- [ ] Consigo criar um novo usuário
- [ ] Consigo entender o fluxo de autenticação
- [ ] Consigo navegar pela estrutura do banco
- [ ] Consigo usar Docker
- [ ] Consigo entender modelos e serializers

---

**Documentação criada para facilitar implementação e troubleshooting! **

_Última atualização: 13 de Maio de 2026_
