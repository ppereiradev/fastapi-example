import uuid as _uuid
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.models.person import Person
from app.schemas.user import UserResponse, UserLoginResponse, UserCreateRequest, UserUpdateRequest
from app.core.security import get_hash_password
from app.services.person import add_person

# Serviço para usuários


async def get_users(db: AsyncSession) -> list[UserResponse]:
    result = await db.execute(
        select(User)
        .options(joinedload(User.person))
        .execution_options(populate_existing=True)
    )
    users = result.scalars().all()
    return [UserResponse.from_orm(user) for user in users]


async def get_user_by_uuid(
    user_uuid: _uuid.UUID, db: AsyncSession
) -> UserResponse | None:
    result = await db.execute(
        select(User)
        .where(User.uuid == user_uuid)
        .options(joinedload(User.person))
        .execution_options(populate_existing=True)
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return UserResponse.from_orm(user)

async def get_user_by_email_login(
    user_email: str, db: AsyncSession
) -> UserLoginResponse | None:
    result = await db.execute(
        select(User)
        .where(User.email == user_email)
        .execution_options(populate_existing=True)
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return UserLoginResponse.from_orm(user)


async def add_user(user: UserCreateRequest, db: AsyncSession) -> UserResponse:
    print(user.name, user.whatsapp)
    new_person = Person(name=user.name, whatsapp=user.whatsapp)
    await add_person(new_person, db)
    encrypted_password = get_hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        encrypted_password=encrypted_password,
        person_id=new_person.id,
    )
    db.add(new_user)

    try:
        await db.commit()
        await db.refresh(new_user, ["person"])
        return UserResponse.from_orm(new_user)
    except IntegrityError as e:
        await db.rollback()  # Reverte as alterações

        # Extrai mensagem do erro
        error_message = str(e.orig).lower()

        if (
            "app_user_username_key" in error_message
        ):  # Verifica se o erro veio do campo username
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="O username de usuário já está em uso.",
            )
        elif (
            "app_user_email_key" in error_message
        ):  # Verifica se o erro veio do campo email
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="O e-mail já está em uso."
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao criar usuário. Verifique os dados e tente novamente.",
            )


async def update_user(
    user_uuid: _uuid.UUID, user_update: UserUpdateRequest, db: AsyncSession
) -> UserResponse:
    result = await db.execute(select(User).where(User.uuid == user_uuid))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.username = user_update.username
    user.email = user_update.email
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(user_uuid: _uuid.UUID, db: AsyncSession) -> None:
    result = await db.execute(select(User).where(User.uuid == user_uuid))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()
    return None
