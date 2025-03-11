from app.db.session import AsyncSessionLocal


# Dependência para injetar o DB nas rotas
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
