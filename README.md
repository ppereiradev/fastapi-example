Sugestão de module-based architecture.

Projetos menores:
```bash
my_api/
│── core/                      # Camada central da aplicação
│   ├── user/                  # Contexto "Usuário"
│   │   ├── models.py          # Define a entidade User (SQLAlchemy)
│   │   └── schemas.py         # Define os esquemas Pydantic (validação e resposta)
│   ├── product/               # Contexto "Produto"
│   │   ├── models.py          # Define a entidade Product
│   │   └── schemas.py         # Define os esquemas Pydantic para Product
│   └── ...                    # Pode incluir mais módulos de domínio (ex: orders, payments, etc.)
│
│── api/                       # Camada de interface da API
│   ├── v1/                    # Versão 1 da API
│   │   ├── endpoints/         # Endpoints organizados por recurso
│   │   │   ├── user.py        # Rotas relacionadas a usuários (ex: /users, /users/{id})
│   │   │   ├── product.py     # Rotas relacionadas a produtos (ex: /products, /products/{id})
│   │   │   └── ...            # Outros endpoints (ex: /orders, /auth)
│   │   └── api.py             # Arquivo que centraliza os routers da API
│   └── ...                    # Pode incluir versões futuras (v2, v3)
│
│── db/                        # Gerenciamento da camada de banco de dados
│   ├── session.py             # Configuração do SQLAlchemy (SessionLocal, engine)
│   └── base.py                # Base para modelos SQLAlchemy (declarative_base)
│
│── main.py                    # Ponto de entrada da aplicação FastAPI
│
└── config.py                  # Configurações globais (ex: variáveis de ambiente credenciais)
```

Projetos maiores:
```bash
my_fastapi_project/
│── app/
│   ├── api/                     # Interface com o mundo externo (Controllers / Routers)
│   │   ├── v1/                   # Versão da API
│   │   │   ├── endpoints/        # Endpoints organizados por recurso
│   │   │   │   ├── users.py      # Endpoints relacionados a usuários
│   │   │   │   ├── auth.py       # Endpoints de autenticação
│   │   │   ├── dependencies.py   # Dependências compartilhadas
│   │   │   ├── __init__.py
│   │   ├── __init__.py
│   ├── core/                     # Configurações centrais da aplicação
│   │   ├── config.py             # Configurações gerais
│   │   ├── security.py           # Configuração de segurança (JWT, OAuth, etc.)
│   │   ├── database.py           # Conexão com banco de dados
│   │   ├── __init__.py
│   ├── domain/                   # Camada de domínio (Entidades, Aggregates, Value Objects)
│   │   ├── user/                  # Bounded Context "User"
│   │   │   ├── models.py         # Entidades e Value Objects de User
│   │   │   ├── interfaces.py     # Interfaces (Repositories, Services)
│   │   │   ├── __init__.py
│   │   ├── __init__.py
│   ├── application/              # Casos de uso (Application Layer)
│   │   ├── user/
│   │   │   ├── commands.py       # Comandos para ações do usuário (CreateUser, DeleteUser, etc.)
│   │   │   ├── queries.py        # Consultas para recuperação de dados
│   │   │   ├── services.py       # Serviços da aplicação
│   │   │   ├── __init__.py
│   │   ├── __init__.py
│   ├── infrastructure/           # Implementações específicas de infraestrutura (ORM, Cache, etc.)
│   │   ├── repositories/         # Implementações de repositórios
│   │   │   ├── user_repository.py # Implementação do repositório de usuários
│   │   │   ├── __init__.py
│   │   ├── external_services/    # Integrações com serviços externos
│   │   │   ├── payment_gateway.py
│   │   │   ├── __init__.py
│   │   ├── __init__.py
│   ├── schemas/                  # Esquemas Pydantic para validação
│   │   ├── user.py               # Schemas para User
│   │   ├── __init__.py
│   ├── main.py                   # Ponto de entrada da aplicação
│   ├── __init__.py
│── tests/                        # Testes unitários e de integração
│   ├── test_api/
│   ├── test_application/
│   ├── test_domain/
│   ├── test_infrastructure/
│   ├── __init__.py
│── docker-compose.yml            # Configuração do Docker Compose
│── requirements.txt              # Dependências do projeto
│── .env                          # Variáveis de ambiente
│── .gitignore
```
