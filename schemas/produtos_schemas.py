from typing import Optional
from datetime import date

from pydantic import BaseModel as SCBaseModel, ConfigDict


class ProdutosBase(SCBaseModel):
    nome: str
    categoria: str
    preço_unitario: float


class ProdutosCreate(ProdutosBase):
    pass


class ProdutosUpdate(ProdutosBase):
    pass


class ProdutosSchema(ProdutosBase):
    id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)