from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.db import get_db
from app.schemas.auth import LoginRequest
from app.services.auth import get_token


router = APIRouter()

@router.post("/")
async def authenticate(user: LoginRequest, db: AsyncSession = Depends(get_db)) -> str:
    token = await get_token(user, db)
    return token
