from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.produtos_models import ProdutosModel
from schemas.produtos_schemas import ProdutosSchema, ProdutosCreate, ProdutosUpdate
from core.deps import get_session


router = APIRouter()


# POST produtos
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ProdutosSchema)
async def post_produtos(produtos: ProdutosCreate, db: AsyncSession = Depends(get_session)):
    novo_produto = ProdutosModel(
        nome=produtos.nome,
        categoria=produtos.categoria,
        preço_unitario=produtos.preço_unitario
    )

    db.add(novo_produto)
    await db.commit()
    await db.refresh(novo_produto)

    return novo_produto


# GET produtos
@router.get('/', response_model=List[ProdutosSchema])
async def get_produtos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProdutosModel)
        result = await session.execute(query)
        produtos: List[ProdutosModel] = result.scalars().all()

        return produtos


# GET produtos
@router.get('/{produto_id}', response_model=ProdutosSchema, status_code=status.HTTP_200_OK)
async def get_produto(produto_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProdutosModel).filter(ProdutosModel.id == produto_id)
        result = await session.execute(query)
        produto = result.scalar_one_or_none()

        if produto:
            return produto
        else:
            raise HTTPException(detail='Produto não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)


# PUT produto
@router.put('/{produto_id}', response_model=ProdutosSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_produto(produto_id: int, produto: ProdutosUpdate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProdutosModel).filter(ProdutosModel.id == produto_id)
        result = await session.execute(query)
        produto_up = result.scalar_one_or_none()

        if produto_up:
            produto_up.nome = produto.nome
            produto_up.categoria = produto.categoria
            produto_up.preço_unitario = produto.preço_unitario

            await session.commit()
            await session.refresh(produto_up)

            return produto_up
        else:
            raise HTTPException(detail='Produto não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)


# DELETE produto
@router.delete('/{produto_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_produto(produto_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProdutosModel).filter(ProdutosModel.id == produto_id)
        result = await session.execute(query)
        produto_del = result.scalar_one_or_none()

        if produto_del:
            await session.delete(produto_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Produto não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)