from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user import get_user_by_email_login
from app.schemas.auth import LoginRequest
from app.core.security import verify_password, create_access_token

async def get_token(user: LoginRequest, db: AsyncSession) -> str:
    if await authenticate_user(user.email, user.password, db):
        return create_access_token(user.dict())
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

async def authenticate_user(user_email: str, user_password: str, db: AsyncSession) -> bool:
    user_from_db = await get_user_by_email_login(user_email, db)
    return verify_password(user_password, user_from_db.encrypted_password)
