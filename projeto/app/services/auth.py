from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user import get_user_by_email_login
from app.schemas.auth import LoginRequest
from app.core.security import verify_password, create_access_token


async def get_token(user: LoginRequest, db: AsyncSession) -> str:
    user_from_db = await get_user_by_email_login(user.email, db)

    if user_from_db and verify_password(user.password, user_from_db.encrypted_password):
        return create_access_token(user_from_db.dict(include={"email", "role"}))
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
