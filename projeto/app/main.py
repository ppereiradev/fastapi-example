import uuid as _uuid
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.init_db import init_db
from app.api.v1.routers import user, auth

app = FastAPI()


@app.on_event("startup")
async def startup():
    await init_db()  # Criar tabelas no banco ao iniciar o app

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
async def root():
    return {"page": "home"}

