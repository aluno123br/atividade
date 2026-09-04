# Checklist de entrega DevShowcase API

## Código e arquitetura

- [x] Projeto FastAPI estruturado
- [x] Repositório preparado com `.gitignore`
- [x] Entidade Profile
- [x] Entidade Project
- [x] Entidade Technology
- [x] Entidade Feedback
- [x] Profile 1:N Project
- [x] Project N:N Technology
- [x] Project 1:N Feedback
- [x] Camada de repositórios
- [x] Camada de serviços
- [x] DTOs de entrada e saída
- [x] Validações de obrigatoriedade e URL

## Endpoints

- [x] POST /api/profiles
- [x] GET /api/profiles/{id}
- [x] POST /api/technologies
- [x] GET /api/technologies
- [x] POST /api/projects
- [x] GET /api/projects
- [x] POST /api/projects/{id}/feedbacks
- [x] PUT /api/projects/{id}/upvote
- [x] Filtro por tecnologia
- [x] Paginação

## Regras avançadas

- [x] Nota de feedback limitada entre 1 e 5
- [x] Média de avaliações recalculada automaticamente
- [x] Incremento de upvotes
- [x] Erro 400 formatado
- [x] Erro 404 formatado
- [x] Tratamento global de exceções
- [x] Swagger/OpenAPI em /docs
- [x] OpenAPI exportado em openapi.json

## Banco e produção

- [x] Suporte a PostgreSQL via DATABASE_URL
- [x] Variáveis de ambiente
- [x] `.env` protegido pelo `.gitignore`
- [x] Docker Compose para PostgreSQL local
- [x] Dockerfile
- [x] render.yaml pronto
- [ ] Criar PostgreSQL na conta do grupo
- [ ] Publicar repositório no GitHub
- [ ] Conectar GitHub ao Render e publicar a API

## Validação

- [x] Testes automatizados criados
- [x] 8 testes executados com sucesso
- [x] Coleção Postman pronta

## Entrega final

- [ ] Inserir link público do GitHub no PDF
- [ ] Inserir link público da API no PDF
- [ ] Gravar vídeo de 5 a 8 minutos
- [ ] Publicar vídeo no YouTube como não listado
- [ ] Inserir link do vídeo no PDF
- [ ] Enviar PDF pelo SIGAA
