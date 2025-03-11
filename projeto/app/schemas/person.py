import uuid as _uuid
from pydantic import BaseModel


class PersonResponse(BaseModel):
    uuid: _uuid.UUID
    name: str
    whatsapp: str

    class Config:
        from_attributes = True  # Permite conversão de ORM para JSON
