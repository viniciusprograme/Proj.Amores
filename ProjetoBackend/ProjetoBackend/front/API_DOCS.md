# 📡 Documentação da API - Amores Instituto

## Base URL
```
http://localhost:8000/api/v1/
```

---

## 🏛️ Endpoints da Instituição

### GET - Obter Informações da Instituição
```http
GET /api/v1/instituicao/principal/
```

**Resposta (200 OK):**
```json
{
  "id": 1,
  "nome": "Amores Instituto",
  "descricao": "O Instituto Amores é uma organização social...",
  "missao": "Promover o bem-estar social...",
  "visao": "Ser referência em transformação social...",
  "valores": "Solidariedade, Empatia, Respeito, Compromisso social, Transparência",
  "chave_pix": "00.000.000/0001-00",
  "tipo_chave_pix": "CNPJ",
  "telefone": "",
  "email": "",
  "endereco": "Sapiranga, Fortaleza–CE"
}
```

---

## 📅 Endpoints de Agendamento

### POST - Criar Novo Agendamento
```http
POST /api/v1/agendamentos/api/
Content-Type: application/json
```

**Body:**
```json
{
  "nome": "João Silva",
  "data_visita": "2026-05-20",
  "horario_preferencial": "09:00:00"
}
```

**Resposta (201 Created):**
```json
{
  "message": "Agendamento realizado com sucesso!",
  "data": {
    "id": 1,
    "nome": "João Silva",
    "data_visita": "2026-05-20",
    "horario_preferencial": "09:00:00"
  }
}
```

### GET - Listar Todos os Agendamentos
```http
GET /api/v1/agendamentos/api/listar/
```

**Resposta (200 OK):**
```json
[
  {
    "id": 1,
    "nome": "João Silva",
    "data_visita": "2026-05-20",
    "horario_preferencial": "09:00:00"
  }
]
```

---

## 🔄 Como Integrar no Frontend

Seu frontend já está pronto! Basta atualizar o arquivo `script.js` para fazer as requisições à API.

Veja o arquivo `api-integration-example.js` para exemplos de como integrar.

---

## 📝 Variáveis de Ambiente

Atualize `.env`:
```
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

---

## ✅ Status dos Endpoints

| Endpoint | Método | Status |
|----------|--------|--------|
| Instituição | GET | ✅ Ativo |
| Agendamento | POST | ✅ Ativo |
| Agendamento | GET | ✅ Ativo |
