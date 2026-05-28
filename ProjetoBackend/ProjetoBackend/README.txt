---PROJETO PRINCIPAL COM APLICAÇÃO DE LOGIN E REGISTRO---

## Estrutura
- `sistemaLogin/` → pasta principal do projeto
  - `settings.py` → configurações do Django
  - `urls.py` → rotas principais
  - `templates/base.html` → layout padrão
- `formulario/` → app de autenticação
  - `views.py` → funções de login, logout, registro, home
  - `urls.py` → rotas da app
  - `templates/formulario/` → páginas específicas (login, registro, home)

## Fluxo de autenticação
- `/login/` → página de login
- `/logout/` → encerra sessão
- `/registro/` → cadastro de novos usuários (opcional)
- `/home/` → página inicial protegida

## Templates
Todas as páginas herdam de `base.html` e usam `{% block content %}` para inserir conteúdo.

## Grupos e permissões
- Grupo "Administradores" → acesso especial
- Grupo "Visitantes" → acesso padrão

---APLICAÇÃO DE AGENDAMENTOS---

## Estrutura de agendamentos
- `models.py` → Classe com nome, data e hora do agendamento
- `forms.py` → Formulário do agendamento
- `views.py` → Funções de criar e listar agendamentos
- `urls.py` → Rotas da app

## Fluxo de agendamento
- `/criar_agendamentos/` → página de criação de agendamento
- `/listar_agendamentos/` → lista de agendamentos

## Administrador
- `admin.py` → Administração de agendamentos
