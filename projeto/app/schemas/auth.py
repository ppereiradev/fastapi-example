from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True  # Permite conversão de ORM para JSON
