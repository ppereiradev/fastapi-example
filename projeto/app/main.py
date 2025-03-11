import uuid as _uuid
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.init_db import init_db
from app.dependencies.db import get_db
from app.services.user import (
    get_users,
    get_user_by_uuid,
    add_user,
    update_user,
    delete_user,
)  # Importação do serviço
from app.schemas.user import UserResponse, UserCreateRequest, UserUpdateRequest
from app.core.security import create_access_token, decode_access_token

app = FastAPI()


@app.on_event("startup")
async def startup():
    await init_db()  # Criar tabelas no banco ao iniciar o app


@app.get("/")
async def root():
    token = create_access_token({"sub": "user@example.com"})

    return {"token": token, "decoded:": decode_access_token(token)}


@app.get("/users/")
async def read_users(db: AsyncSession = Depends(get_db)) -> list[UserResponse]:
    return await get_users(db)  # Chama o serviço para obter os usuários


@app.get("/users/{user_uuid}")
async def read_user(
    user_uuid: _uuid.UUID, db: AsyncSession = Depends(get_db)
) -> UserResponse:
    return await get_user_by_uuid(
        user_uuid, db
    )  # Chama o serviço para obter o usuário pelo ID


@app.post("/users/")
async def create_user(
    user: UserCreateRequest, db: AsyncSession = Depends(get_db)
) -> UserResponse:
    return await add_user(user, db)


@app.put("/users/{user_uuid}")
async def update_user(
    user_uuid: _uuid.UUID,
    user_update: UserUpdateRequest,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    return await update_user(
        user_uuid, user_update, db
    )  # Chama o serviço para atualizar o usuário


@app.delete("/users/{user_uuid}")
async def delete_user(user_uuid: _uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await delete_user(user_uuid, db)
