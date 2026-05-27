# 🚀 Guia de Instalação e Setup

## ✅ Pré-requisitos
- Python 3.8+
- Django 6.0
- pip instalado

---

## 📋 Passos para Setup

### 1️⃣ Instale as dependências

```bash
cd sistemaLogin
pip install -r requirements.txt
```

### 2️⃣ Crie as migrações para a nova app

```bash
python manage.py makemigrations instituicao
python manage.py makemigrations agenda
python manage.py migrate
```

### 3️⃣ Crie um superusuário (Admin)

```bash
python manage.py createsuperuser
```

Siga as instruções e defina:
- Email: admin@amores.com
- Senha: (escolha uma segura)

### 4️⃣ Carregue dados iniciais (Opcional)

```bash
python manage.py shell
```

Dentro do shell:
```python
from apps.instituicao.models import Instituicao

# Criar registro padrão se não existir
instituicao, created = Instituicao.objects.get_or_create(
    nome="Amores Instituto"
)
if created:
    print("✅ Instituição criada com sucesso!")
else:
    print("✅ Instituição já existe")
    
exit()
```

### 5️⃣ Inicie o servidor

```bash
python manage.py runserver
```

O servidor estará disponível em: `http://localhost:8000`

---

## 🔧 Endpoints Disponíveis

### 📚 Documentação da API
- Swagger UI: `http://localhost:8000/api/schema/swagger-ui/`
- ReDoc: `http://localhost:8000/api/schema/redoc/`

### 🏛️ Instituição
- `GET /api/v1/instituicao/principal/` - Dados da instituição

### 📅 Agendamentos
- `POST /api/v1/agendamentos/api/` - Criar agendamento
- `GET /api/v1/agendamentos/api/listar/` - Listar agendamentos

### 🛠️ Admin
- `http://localhost:8000/admin/` - Painel administrativo (login com superusuário)

---

## 🌐 CORS e Frontend

O CORS já está configurado para:
- `http://localhost:3000`
- `http://127.0.0.1:3000`
- `http://localhost:8000`
- `http://127.0.0.1:8000`

Se você servir o frontend em outra porta, atualize `sistemaLogin/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:SUA_PORTA",
    "http://127.0.0.1:SUA_PORTA",
]
```

---

## 📝 Estrutura de Arquivos

```
sistemaLogin/
├── apps/
│   ├── instituicao/          ⭐ NOVA APP
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── admin.py
│   ├── users/
│   ├── products/
│   └── ...
├── agenda/
│   ├── models.py
│   ├── views.py          ⭐ ATUALIZADO
│   ├── serializers.py    ⭐ NOVO
│   ├── urls.py           ⭐ ATUALIZADO
│   └── ...
└── sistemaLogin/
    ├── settings.py       ⭐ ATUALIZADO
    └── urls.py           ⭐ ATUALIZADO
```

---

## 🧪 Testando os Endpoints

### Com cURL

```bash
# Obter informações da instituição
curl http://localhost:8000/api/v1/instituicao/principal/

# Criar agendamento
curl -X POST http://localhost:8000/api/v1/agendamentos/api/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "data_visita": "2026-05-20",
    "horario_preferencial": "09:00:00"
  }'
```

### Com Postman

1. Importe a collection: `MarketSolutionsAPI.postman_collection.json`
2. Adicione as requisições dos novos endpoints

---

## 🐛 Resolução de Problemas

### Erro: "ModuleNotFoundError: No module named 'apps.instituicao'"

**Solução:** Verifique se a app está no `INSTALLED_APPS` em `settings.py`

### Erro: "CORS policy: No 'Access-Control-Allow-Origin'"

**Solução:** 
1. Verifique se a porta do frontend está em `CORS_ALLOWED_ORIGINS`
2. Reinicie o servidor Django

### Erro: "relation \"apps_instituicao_instituicao\" does not exist"

**Solução:** Execute as migrações:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 📞 Suporte

Para mais informações, consulte:
- [API_DOCS.md](API_DOCS.md) - Documentação detalhada dos endpoints
- [api-integration-example.js](api-integration-example.js) - Exemplos de integração
