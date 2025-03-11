import uuid as _uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.db import get_db
from app.services.user import (
    get_users,
    get_user_by_uuid,
    add_user,
    update_user,
    delete_user,
)  # Importação do serviço
from app.schemas.user import UserResponse, UserCreateRequest, UserUpdateRequest
from app.dependencies.security import validate_access_token
from app.dependencies.required_roles import require_roles


router = APIRouter()

@router.get("/", dependencies=[Depends(require_roles(["ADMIN", "USER"]))])
async def read_users(db: AsyncSession = Depends(get_db)) -> list[UserResponse]:
    return await get_users(db)  # Chama o serviço para obter os usuários


@router.get("/{user_uuid}")
async def read_user(
    user_uuid: _uuid.UUID, db: AsyncSession = Depends(get_db)
) -> UserResponse:
    return await get_user_by_uuid(
        user_uuid, db
    )  # Chama o serviço para obter o usuário pelo ID


@router.post("/")
async def create_user(
    user: UserCreateRequest, db: AsyncSession = Depends(get_db)
) -> UserResponse:
    return await add_user(user, db)


@router.put("/{user_uuid}")
async def update_user(
    user_uuid: _uuid.UUID,
    user_update: UserUpdateRequest,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    return await update_user(
        user_uuid, user_update, db
    )  # Chama o serviço para atualizar o usuário


@router.delete("/{user_uuid}")
async def delete_user(user_uuid: _uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await delete_user(user_uuid, db)
