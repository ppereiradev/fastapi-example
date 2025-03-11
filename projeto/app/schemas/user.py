import uuid as _uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.user import User
from app.core.enums import Role


class UserResponse(BaseModel):
    uuid: _uuid.UUID
    email: EmailStr
    name: str
    whatsapp: str
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]

    @classmethod
    def from_orm(cls, user: User):
        return cls(
            uuid=user.uuid,
            email=user.email,
            name=user.person.name,  # Extraindo direto do relacionamento
            whatsapp=user.person.whatsapp,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login=user.last_login,
        )

    class Config:
        from_attributes = True  # Permite conversão de ORM para JSON


class UserLoginResponse(BaseModel):
    email: EmailStr
    role: str
    encrypted_password: str

    class Config:
        from_attributes = True  # Permite conversão de ORM para JSON


class UserCreateRequest(BaseModel):
    name: str
    username: str
    whatsapp: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True  # Permite conversão de ORM para JSON


class UserUpdateRequest(BaseModel):
    username: str
    email: EmailStr

    class Config:
        from_attributes = True  # Permite conversão de ORM para JSON
