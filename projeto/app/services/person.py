from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.models.person import Person
from app.schemas.person import PersonResponse


async def add_person(person: Person, db: AsyncSession) -> Person:
    db.add(person)
    try:
        await db.commit()
        await db.refresh(person)
        return person
    except IntegrityError as e:
        await db.rollback()  # Reverte as alterações

        # Extrai mensagem do erro
        error_message = str(e.orig).lower()

        if (
            "person_whatsapp_key" in error_message
        ):  # Verifica se o erro veio do campo whatsapp
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="O whatsapp já está cadastrado.",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao criar pessoa. Verifique os dados e tente novamente.",
            )


async def update_person(
    person_uuid: int, person_update: Person, db: AsyncSession
) -> PersonResponse:
    result = await db.execute(select(Person).where(Person.uuid == person_uuid))
    person = result.scalars().first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    person.name = person_update.name
    person.email = person_update.email
    await db.commit()
    await db.refresh(person)
    return person


async def delete_person(person_uuid: int, db: AsyncSession) -> None:
    result = await db.execute(select(Person).where(Person.uuid == person_uuid))
    person = result.scalars().first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    await db.delete(person)
    await db.commit()
    return None
