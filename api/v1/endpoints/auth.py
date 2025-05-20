from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import httpx
from core.security import create_access_token, verify_token, ACCESS_TOKEN_EXPIRE_MINUTES
from core.configs import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class LoginResponse(BaseModel):
    user_id: int
    username: str
    email: str
    full_name: str | None = None

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(token)
    if token_data is None:
        raise credentials_exception
    
    # Buscar dados do usuário no microserviço de login
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.LOGIN_SERVICE_URL}/api/v1/users/me",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code == 200:
                user_data = response.json()
                return User(
                    username=user_data["username"],
                    email=user_data["email"],
                    full_name=user_data.get("full_name"),
                    disabled=user_data.get("disabled", False)
                )
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Serviço de login indisponível"
            )
    
    raise credentials_exception

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Autenticar com o microserviço de login
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.LOGIN_SERVICE_URL}/api/v1/auth/login",
                data={
                    "username": form_data.username,
                    "password": form_data.password
                }
            )
            
            if response.status_code == 200:
                login_data = response.json()
                # Criar token JWT com os dados do usuário
                access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = create_access_token(
                    data={"sub": login_data["username"]},
                    expires_delta=access_token_expires
                )
                return {"access_token": access_token, "token_type": "bearer"}
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Serviço de login indisponível"
            )

@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user 