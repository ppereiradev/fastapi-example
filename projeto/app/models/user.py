import uuid as _uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime, func
from sqlalchemy import String, BigInteger
from app.db.base import Base
from datetime import datetime
from app.core.enums import Role


class User(Base):

    __tablename__ = "app_user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    uuid: Mapped[_uuid.UUID] = mapped_column(
        UUID(as_uuid=True), unique=True, default=_uuid.uuid4
    )
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    encrypted_password: Mapped[str]
    role: Mapped[Role] = mapped_column(default=Role.USER)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.timezone("UTC", func.now())
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.timezone("UTC", func.now()),
        onupdate=func.timezone("UTC", func.now()),
    )
    last_login: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    # Definição da chave estrangeira para a tabela "person"
    person_id: Mapped[int] = mapped_column(ForeignKey("person.id"), nullable=False)

    # Relacionamento com a tabela Person (opcional)
    person: Mapped["Person"] = relationship("Person", back_populates="user")
