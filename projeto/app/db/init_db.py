from app.db.session import async_engine
from app.models.user import User
from app.models.person import Person
from app.db.base import Base


# Função para criar as tabelas no banco de dados
async def init_db():
    async with async_engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
