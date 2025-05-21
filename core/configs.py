from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from typing import ClassVar


class Settings(BaseSettings):
    """
    Configurações gerais usadas na aplicação
    """

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = 'UrbanFood - Microserviço de Produtos'
    # filepath: /home/galaxybook2/Documentos/repositorio/famp/secao04/core/configs.py
    # DB_URL: str = "postgresql+asyncpg://teste_user:ollpemjnlwsg@db-57878.dc-sp-1.absamcloud.com:11087/teste"
    DB_URL: str = (
        "postgresql+asyncpg://postgres.tascqincqdsjvmdjdwnh:123456@aws-0-us-east-2.pooler.supabase.com:5432/postgres"
    )

    # URLs dos microserviços
    LOGIN_SERVICE_URL: str = 'http://localhost:8001'  # URL do microserviço de login

    DBBaseModel: ClassVar = (
        declarative_base()
    )  # Adicionando ClassVar para evitar o erro

    class Config:
        case_sensitive = True


settings = Settings()