from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from typing import ClassVar


class Settings(BaseSettings):
    """
    Configurações gerais usadas na aplicação
    """

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = 'UrbanFood - Microserviço de Produtos'
    DB_URL: str = (
        "mysql+aiomysql://urbanfood:Urbanf00dFiap@rds-mysql.c8gkm8vsq6yc.us-east-1.rds.amazonaws.com:3306/urbanfood"
    )

    DBBaseModel: ClassVar = (
        declarative_base()
    )  # Adicionando ClassVar para evitar o erro

    # URL do microserviço de login
    #LOGIN_SERVICE_URL: str = 'http://localhost:8001'
    LOGIN_SERVICE_URL: str = 'http://a290354dd0cfd40cbb428316c51cd3ea-2025820054.us-east-1.elb.amazonaws.com:8001'

    class Config:
        case_sensitive = True

settings = Settings()