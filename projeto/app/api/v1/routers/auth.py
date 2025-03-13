from fastapi import APIRouter, Depends, HTTPException
import httpx
from app.core.security import create_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.db import get_db
from app.schemas.auth import LoginRequest, LoginResponse
from app.services.auth import get_token
from app.core.config import settings

# Importação do formulário de autenticação do FastAPI no Swagger
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()


@router.post("/")
async def authenticate(
    user: LoginRequest, db: AsyncSession = Depends(get_db)
) -> LoginResponse:
    token = await get_token(user, db)
    return LoginResponse(access_token=token)


@router.post("/swagger")
async def get_token_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    email = form_data.username
    password = form_data.password
    user = LoginRequest(email=email, password=password)
    token = await get_token(user, db)
    return {"access_token": token}


@router.get("/github")
async def login_github():
    """Retorna a URL para o usuário fazer login via GitHub"""
    return {
        "url": f"{settings.GITHUB_OAUTH_URL}?client_id={settings.GITHUB_CLIENT_ID}&scope=user"
    }


@router.get("/github/callback")
async def auth_callback(code: str, db: AsyncSession = Depends(get_db)) -> LoginResponse:
    """Troca o código de autorização do GitHub por um token de acesso"""

    # Obter token de acesso do GitHub
    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.GITHUB_TOKEN_URL,
            headers={"Accept": "application/json"},
            data={
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": code,
            },
        )

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Erro ao obter token")

    token_data = response.json()
    access_token = token_data.get("access_token")

    if not access_token:
        raise HTTPException(status_code=400, detail="Token inválido")

    # Obter informações do usuário do GitHub
    async with httpx.AsyncClient() as client:
        response = await client.get(
            settings.GITHUB_API_URL,
            headers={"Authorization": f"Bearer {access_token}"},
        )

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Erro ao obter dados do usuário")

    user_data = response.json()
    email = user_data.get("email")
    username = user_data.get("login")

    if not email:
        email = f"{username}@github.com"  # O GitHub nem sempre retorna email público

    # Criar um token JWT para o usuário autenticado via GitHub
    jwt_token = create_access_token({"email": email, "role": "USER"})

    return LoginResponse(access_token=jwt_token)
