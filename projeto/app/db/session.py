from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Criando um engine assíncrono
async_engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Criando uma fábrica de sessões assíncronas
AsyncSessionLocal = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)
