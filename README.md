# DevShowcase API

Projeto acadêmico de Programação Backend para gerenciamento de perfis de desenvolvedores, projetos, tecnologias, feedbacks e curtidas.

## Tecnologias utilizadas

- Python 3.12
- FastAPI
- SQLAlchemy 2
- Pydantic 2
- PostgreSQL em produção
- SQLite apenas como opção rápida para desenvolvimento local
- Swagger/OpenAPI
- Pytest
- Render para deploy

## Requisitos atendidos

- Entidade Profile
- Entidade Project
- Entidade Technology
- Entidade Feedback
- Relacionamento Profile 1:N Project
- Relacionamento Project N:N Technology
- Relacionamento Project 1:N Feedback
- Repositórios de persistência
- DTOs de entrada e saída
- Validação de campos obrigatórios
- Validação de URLs
- Cadastro e consulta de perfis
- Cadastro e listagem de tecnologias
- Cadastro e listagem de projetos
- Feedback com nota de 1 a 5
- Atualização automática da média do projeto
- Upvote de projetos
- Filtro de projetos por tecnologia
- Paginação
- Tratamento global de erros 400 e 404
- Documentação Swagger/OpenAPI
- Configuração por variáveis de ambiente
- Arquivo render.yaml para deploy
- Testes automatizados
- Coleção do Postman

## Estrutura do projeto

```text
devshowcase_api/
  app/
    api/routes/
    core/
    models/
    repositories/
    schemas/
    services/
    database.py
    main.py
  postman/
  scripts/
  tests/
  .env.example
  .gitignore
  Dockerfile
  docker-compose.yml
  render.yaml
  requirements.txt
  requirements-dev.txt
  README.md
```

## Execução rápida local

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Swagger: `http://127.0.0.1:8000/docs`

Health check: `http://127.0.0.1:8000/health`

## Deploy no Render

O arquivo `render.yaml` já está preparado. No Render, conecte este repositório, configure a variável `DATABASE_URL` e publique o serviço.

Build Command: `pip install -r requirements.txt`

Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Endpoints

### Profile

```http
POST /api/profiles
GET /api/profiles/{id}
```

### Technology

```http
POST /api/technologies
GET /api/technologies
```

### Project

```http
POST /api/projects
GET /api/projects
```

Filtro e paginação:

```http
GET /api/projects?technology=Python&page=0&size=10
```

### Feedback

```http
POST /api/projects/{id}/feedbacks
```

### Upvote

```http
PUT /api/projects/{id}/upvote
```

## Testes automatizados

Execute:

```bash
pytest -q
```

Validação realizada: **8 testes aprovados**.

## Postman

Importe `postman/DevShowcase_API.postman_collection.json`.

## Aluno

Augusto Martins Campos Júnior

## Disciplina

Programação Backend, Universidade Aberta do Piauí (UAPI).
