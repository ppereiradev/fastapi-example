Sugestão de module-based architecture.

```bash
app/
├── api/
│   ├── v1/
│   │   ├── users/
│   │   │   ├── routes.py  # Endpoints
│   │   │   ├── schemas.py # Pydantic/SQLModel
│   │   │   ├── services.py # Regras de negócio (caso precise)
│   │   │   ├── repository.py # Acesso ao banco
│   │   │   ├── models.py # SQLAlchemy
│   │   ├── posts/
│   │   ├── orders/
│   │   ├── auth/
├── core/
│   ├── database.py # Conexão com o banco
│   ├── config.py   # Configurações globais
│   ├── security.py # Autenticação e segurança
├── tests/
│   ├── test_users.py
│   ├── test_orders.py
```
