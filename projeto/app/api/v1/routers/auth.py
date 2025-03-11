from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.db import get_db
from app.schemas.auth import LoginRequest, LoginResponse
from app.services.auth import get_token


router = APIRouter()

@router.post("/")
async def authenticate(user: LoginRequest, db: AsyncSession = Depends(get_db)) -> LoginResponse:
    token = await get_token(user, db)
    return LoginResponse(access_token=token)
