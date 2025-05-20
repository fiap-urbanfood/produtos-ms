from core.configs import settings
from sqlalchemy import Column, Integer, String


class ProdutosModel(settings.DBBaseModel):
     __tablename__= 'produtos'

     id = Column(Integer, primary_key=True, autoincrement=True)
     nome = Column(String(256), nullable=True)
     categoria = Column(String(256), nullable=True)
     preço_unitario = Column(Integer, nullable=True)