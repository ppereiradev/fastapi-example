from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.user import User
from app.models.person import Person
from app.db.base import Base


# Criando um engine assíncrono
async_engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Criando uma fábrica de sessões assíncronas
AsyncSessionLocal = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


# Função para criar as tabelas no banco de dados
async def init_db():
    async with async_engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# Fecha todas as conexões do banco ao encerrar a aplicação
async def close_db():
    await async_engine.dispose()
