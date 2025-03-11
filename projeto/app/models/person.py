import uuid as _uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, String
from app.db.base import Base
from typing import List


class Person(Base):

    __tablename__ = "person"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    uuid: Mapped[_uuid.UUID] = mapped_column(
        UUID(as_uuid=True), unique=True, default=_uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    whatsapp: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)

    # Relacionamento com User
    user: Mapped["User"] = relationship("User", back_populates="person")
