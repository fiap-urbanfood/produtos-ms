from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import httpx
import logging
from core.security import create_access_token, verify_token, ACCESS_TOKEN_EXPIRE_MINUTES
from core.configs import settings

# Configurando logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

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
    logger.info(f"Token recebido em get_current_user: {token}")
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(token)
    logger.info(f"Resultado da verificação do token: {token_data}")
    if token_data is None:
        raise credentials_exception
    
    # Buscar dados do usuário no microserviço de login
    async with httpx.AsyncClient() as client:
        try:
            user_info_url = f"{settings.LOGIN_SERVICE_URL}/api/v1/usuarios/logado"  # URL atualizada
            # Não enviaremos payload no corpo ou query params, apenas o token no cabeçalho

            logger.info(f"Tentando obter dados do usuário em: {user_info_url}")
            logger.info(f"Método: GET")
            logger.info(f"Token enviado no cabeçalho: {token}")

            response = await client.get(
                user_info_url,
                headers={
                    "Authorization": f"Bearer {token}" # Enviando apenas o token no cabeçalho
                    # Remover Content-Type se não for necessário, mas vamos manter por enquanto
                }
            )

            logger.info(f"Resposta do serviço de login /logado - Status: {response.status_code}")
            logger.info(f"Resposta do serviço de login /logado - Conteúdo: {response.text}")

            if response.status_code == 200:
                user_data = response.json()
                # Precisamos ajustar a extração dos campos username, email, etc.
                # com base na resposta real deste endpoint
                # Por enquanto, vamos tentar extrair 'username' como antes
                return User(
                    username=user_data.get("username", user_data.get("email", "")), # Tentando username ou email
                    email=user_data.get("email"),
                    full_name=user_data.get("full_name"),
                    disabled=user_data.get("disabled", False)
                )

            # Se a resposta não for 200, levanta HTTPException
            error_detail = "Erro ao obter dados do usuário logado"
            try:
                error_data = response.json()
                if "detail" in error_data:
                    error_detail = error_data["detail"]
            except:
                pass # Ignora erro ao parsear JSON se a resposta não for JSON

            raise HTTPException(
                status_code=response.status_code, # Usar o status code da resposta do login service
                detail=error_detail,
                headers={"WWW-Authenticate": "Bearer"} if response.status_code == status.HTTP_401_UNAUTHORIZED else None
            )

        except httpx.RequestError as e:
            logger.error(f"Erro na requisição ao serviço de login /logado: {str(e)}")
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
            # Ajustando a URL para o endpoint correto do serviço de login
            login_url = f"{settings.LOGIN_SERVICE_URL}/api/v1/usuarios/login"  # Adicionando /login novamente
            login_data = {
                "username": form_data.username,
                "password": form_data.password
            }
            
            logger.info(f"Tentando login em: {login_url}")
            logger.info(f"Dados de login: {login_data}")
            logger.info(f"Método: POST")
            
            response = await client.post(
                login_url,
                data=login_data,  # Mudando de json para data
                headers={"Content-Type": "application/x-www-form-urlencoded"}  # Ajustando o header
            )
            
            logger.info(f"Resposta do serviço de login - Status: {response.status_code}")
            logger.info(f"Resposta do serviço de login - Conteúdo: {response.text}")
            
            if response.status_code == 200:
                login_data = response.json()
                # Criar token JWT com os dados do usuário
                access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = create_access_token(
                    data={"sub": login_data.get("email", form_data.username)},
                    expires_delta=access_token_expires
                )
                return {"access_token": access_token, "token_type": "bearer"}
            
            # Se chegou aqui, o login falhou
            error_detail = "Usuário ou senha incorretos"
            try:
                error_data = response.json()
                if "detail" in error_data:
                    error_detail = error_data["detail"]
            except:
                pass
                
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_detail,
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        except httpx.RequestError as e:
            logger.error(f"Erro na requisição ao serviço de login: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Serviço de login indisponível"
            )

@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user 