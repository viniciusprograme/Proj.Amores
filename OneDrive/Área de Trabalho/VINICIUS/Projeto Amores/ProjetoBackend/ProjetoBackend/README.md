# Market Solutions Platform - Backend API

Uma plataforma completa de soluções de mercado construída com Django REST Framework, oferecendo autenticação JWT, gerenciamento de produtos e categorias.

##  Funcionalidades

-  **Autenticação JWT** - Login/registro seguro com tokens
-  **Modelo de Usuário Customizado** - Sem username, usa email como identificador
-  **Gerenciamento de Produtos** - CRUD completo com categorias
-  **API RESTful** - Endpoints bem documentados
-  **Documentação Interativa** - Swagger UI e ReDoc
-  **Admin Django** - Interface administrativa
-  **Configuração Docker** - Pronto para produção
-  **Testes** - Suite de testes incluída
-  **Postman Collection** - Para testar a API

##  Pré-requisitos

- Python 3.8+
- pip
- virtualenv (recomendado)

##  Instalação e Configuração

### 1. Clonagem e Ambiente Virtual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Arquivo .env

Crie um arquivo `.env` na raiz do projeto `sistemaLogin/`:

```env
# Django Settings
SECRET_KEY=your-super-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7

# Email (opcional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### 3. Migrações e Superusuário

```bash
# Executar migrações
python manage.py migrate

# Criar superusuário
python manage.py shell -c "from apps.users.models import User; User.objects.create_superuser('admin@marketsolutions.com', 'Admin123!', first_name='Admin', last_name='User')"
```

### 4. Executar Servidor

```bash
python manage.py runserver
```

A API estará disponível em: http://localhost:8000

##  Documentação da API

### Endpoints Principais

#### Autenticação
- `POST /api/v1/users/auth/register/` - Registrar usuário
- `POST /api/v1/users/auth/login/` - Login
- `GET /api/v1/users/me/` - Perfil do usuário atual

#### Produtos
- `GET /api/v1/products/public/featured/` - Produtos em destaque (público)
- `GET /api/v1/products/public/search/?q=termo` - Buscar produtos (público)
- `GET /api/v1/products/products/` - Listar produtos (autenticado)
- `POST /api/v1/products/products/` - Criar produto (autenticado)

#### Categorias
- `GET /api/v1/products/categories/` - Listar categorias

### Documentação Interativa
- **Swagger UI**: http://localhost:8000/api/schema/swagger-ui/
- **ReDoc**: http://localhost:8000/api/schema/redoc/

##  Testes

```bash
# Executar todos os testes
python manage.py test

# Executar testes específicos
python manage.py test tests.test_users
python manage.py test tests.test_products
```

##  Docker (Produção)

```bash
# Construir imagem
docker build -t market-solutions .

# Executar container
docker run -p 8000:8000 market-solutions
```

##  Postman Collection

Importe o arquivo `MarketSolutionsAPI.postman_collection.json` no Postman para testar todos os endpoints.

### Fluxo de Teste:
1. **Registrar usuário** ou usar credenciais do admin
2. **Fazer login** para obter tokens
3. **Definir variável `access_token`** no Postman
4. **Testar endpoints** autenticados

##  Estrutura do Projeto

```
sistemaLogin/
├── core/                    # App core com middleware
├── apps/
│   ├── users/              # Gerenciamento de usuários
│   ├── products/           # Produtos e categorias
│   ├── authentication/     # Autenticação adicional
│   └── common/             # Utilitários comuns
├── sistemaLogin/           # Configurações Django
├── tests/                  # Testes
├── scripts/                # Scripts utilitários
├── Dockerfile              # Configuração Docker
├── docker-compose.yml      # Orquestração
├── requirements.txt        # Dependências Python
└── pytest.ini             # Configuração de testes
```

##  Credenciais Padrão

- **Email**: admin@marketsolutions.com
- **Senha**: Admin123!
- **Painel Admin**: http://localhost:8000/admin/

##  Notas de Desenvolvimento

- O projeto usa **email como identificador único** (sem username)
- **JWT tokens** são usados para autenticação
- **SQLite** é usado por padrão (fácil para desenvolvimento)
- **CORS** está habilitado para desenvolvimento frontend
- **Logs** são salvos em `logs/` directory

##  Próximos Passos

1. **Testar todos os endpoints** com Postman
2. **Configurar banco PostgreSQL** para produção
3. **Implementar frontend** (React/Vue/Angular)
4. **Adicionar mais funcionalidades** (pedidos, pagamentos, etc.)
5. **Configurar CI/CD** pipeline

---

**Desenvolvido com Django REST Framework**