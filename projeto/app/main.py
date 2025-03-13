import uuid as _uuid
from fastapi import FastAPI, APIRouter
from app.api.v1.routers import user, auth
from contextlib import asynccontextmanager
from app.db.session import init_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  # Cria as tabelas
    yield  # Deixa a aplicação rodar
    await close_db()  # Fecha conexões do banco ao encerrar


app = FastAPI(lifespan=lifespan)

# Crie o APIRouter com o prefixo '/api/v1'
api_v1_router = APIRouter()

# Registre outros routers dentro do router api_v1_router
api_v1_router.include_router(user.router, prefix="/users", tags=["users"])
api_v1_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Inclua o router global na aplicação
app.include_router(api_v1_router, prefix="/api/v1")
