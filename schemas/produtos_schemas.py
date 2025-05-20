from typing import Optional
from datetime import date

from pydantic import BaseModel as SCBaseModel


class ProdutosSchema(SCBaseModel):
    id: Optional[int]
    nome: str
    categoria: str
    preço_unitario: int

    class Config:
        orm_mode = True