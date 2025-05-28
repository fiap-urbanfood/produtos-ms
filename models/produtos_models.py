from sqlalchemy import Column, Integer, String, Float
from models.base_model import Base


class ProdutosModel(Base):
    __tablename__ = 'produtos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(256), nullable=False)
    categoria = Column(String(256), nullable=False)
    preço_unitario = Column(Float, nullable=False)