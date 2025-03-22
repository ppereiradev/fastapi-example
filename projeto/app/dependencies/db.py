from app.db.session import AsyncSessionLocal
from sqlalchemy.exc import SQLAlchemyError


# Dependência para injetar o DB nas rotas
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()  # Commit da transação se tudo der certo
        except SQLAlchemyError as e:
            await session.rollback()  # Rollback em caso de erro
            raise
