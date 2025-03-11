import uuid as _uuid
from fastapi import FastAPI, APIRouter
from app.db.init_db import init_db
from app.api.v1.routers import user, auth

app = FastAPI()


@app.on_event("startup")
async def startup():
    await init_db()  # Criar tabelas no banco ao iniciar o app


# Crie o APIRouter com o prefixo '/api/v1'
api_v1_router = APIRouter()

# Registre outros routers dentro do router api_v1_router
api_v1_router.include_router(user.router, prefix="/users", tags=["users"])
api_v1_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Inclua o router global na aplicação
app.include_router(api_v1_router, prefix="/api/v1")
