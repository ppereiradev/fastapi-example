from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True  # Permite conversão de ORM para JSON

class LoginResponse(BaseModel):
    access_token: str

    class Config:
        from_attributes = True  # Permite conversão de ORM para JSON
